from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ai_commerce_engine.models import (
    AuditLog,
    Evidence,
    Opportunity,
    Product,
    ProductVersion,
    ScoreSnapshot,
    StatusHistory,
    SupplierOffer,
    ValidationExperiment,
)
from ai_commerce_engine.repositories.products import (
    append_evidence,
    create_product,
    import_products,
    list_products,
)
from ai_commerce_engine.schemas import (
    EvidenceCreate,
    OpportunityCreate,
    ProductCreate,
    ProductEdit,
    StatusChange,
)
from ai_commerce_engine.services.audit import record_audit
from ai_commerce_engine.services.economics import EconomicsInputs, calculate_unit_economics
from ai_commerce_engine.services.experiments import derived_experiment_metrics
from ai_commerce_engine.services.opportunities import (
    convert_opportunity_to_product,
    create_opportunity,
)
from ai_commerce_engine.services.product_versions import edit_product, rollback_product
from ai_commerce_engine.services.recommendations import (
    DeterministicRecommendationGenerator,
    render_recommendation_json,
    render_recommendation_markdown,
)
from ai_commerce_engine.services.research import (
    RESEARCH_SECTIONS,
    assess_research,
    export_research_report,
    latest_research_entries,
    save_research_entry,
)
from ai_commerce_engine.services.scores import save_score
from ai_commerce_engine.services.scoring import DEFAULT_WEIGHTS, PENALTY_FIELDS
from ai_commerce_engine.services.settings import get_scoring_weights, save_scoring_weights
from ai_commerce_engine.services.workflow import PIPELINE_STATUSES, change_status
from ai_commerce_engine.ui.components import empty_state, money_label, page_header


def _product_options(session: Session) -> dict[str, int]:
    return {f"{item.name} · #{item.id}": item.id for item in list_products(session)}


def _selected_product(session: Session, key: str) -> Product | None:
    options = _product_options(session)
    if not options:
        empty_state("Add a product in Product pipeline to begin.")
        return None
    label = st.selectbox("Product", options, key=key)
    return session.get(Product, options[label])


def executive_overview(session: Session) -> None:
    page_header("Executive overview", "Portfolio health, evidence coverage, and decision momentum.")
    products = list_products(session)
    evidence_count = session.scalar(select(func.count(Evidence.id))) or 0
    active_tests = (
        session.scalar(
            select(func.count(ValidationExperiment.id)).where(
                ValidationExperiment.end_date.is_(None)
            )
        )
        or 0
    )
    avg_score = session.scalar(select(func.avg(ScoreSnapshot.final_score)))
    columns = st.columns(4)
    columns[0].metric("Opportunities", len(products))
    columns[1].metric("Evidence records", evidence_count)
    columns[2].metric("Open experiments", active_tests)
    columns[3].metric("Average score", f"{float(avg_score or 0):.1f}")
    if not products:
        empty_state(
            "No products yet. Use Product pipeline to create or import the first opportunity."
        )
        return
    frame = pd.DataFrame([{"Product": p.name, "Status": p.status} for p in products])
    counts = frame.groupby("Status", as_index=False).size()
    st.plotly_chart(
        px.bar(counts, x="Status", y="size", title="Pipeline distribution"),
        use_container_width=True,
    )


def opportunity_vault(session: Session) -> None:
    page_header(
        "Opportunity Vault",
        "Capture unusual observations quickly before deciding whether they are products.",
    )
    quick, vault = st.tabs(["Rapid entry", "Vault"])
    with quick, st.form("opportunity_quick_entry", clear_on_submit=True):
        title = st.text_input("Title *", placeholder="What caught your attention?")
        observation = st.text_area(
            "Observation *", placeholder="Record what you actually saw, not the conclusion."
        )
        columns = st.columns(3)
        source = columns[0].text_input("Source *", value="Manual observation")
        observed = columns[1].date_input("Date observed", value=date.today())
        confidence = columns[2].selectbox("Evidence confidence", ["Low", "Medium", "High"])
        abnormal = st.checkbox("Things That Shouldn't Be True")
        unusual = st.text_area("Why it appears unusual")
        with st.expander("Optional context"):
            source_url = st.text_input("Source URL")
            attachment = st.text_input("Screenshot or attachment reference")
            problem = st.text_area("Customer problem or desire")
            market = st.text_input("Location or market")
            category = st.text_input("Possible category")
            customer = st.text_input("Possible customer")
            hypothesis = st.text_area("Initial hypothesis")
            tags = st.text_input("Tags, comma-separated")
            questions = st.text_area("Follow-up questions")
        if st.form_submit_button("Save to Inbox", type="primary"):
            try:
                created = create_opportunity(
                    session,
                    OpportunityCreate(
                        title=title,
                        observation=observation,
                        unusual_reason=unusual or None,
                        customer_problem=problem or None,
                        source=source,
                        source_url=source_url or None,
                        attachment_reference=attachment or None,
                        observed_date=observed,
                        market=market or None,
                        possible_category=category or None,
                        possible_customer=customer or None,
                        initial_hypothesis=hypothesis or None,
                        tags=tags.split(","),
                        evidence_confidence=confidence,
                        submitted_by="user",
                        follow_up_questions=questions or None,
                        things_that_shouldnt_be_true=abnormal,
                    ),
                )
                session.commit()
                st.success(f"Saved opportunity #{created.id} to Inbox.")
            except (ValidationError, ValueError) as exc:
                session.rollback()
                st.error(str(exc))
    with vault:
        opportunities = list(
            session.scalars(select(Opportunity).order_by(Opportunity.created_at.desc()))
        )
        if not opportunities:
            empty_state("The vault is empty. Capture an observation in Rapid entry.")
            return
        st.dataframe(
            [
                {
                    "ID": item.id,
                    "Title": item.title,
                    "Status": item.status,
                    "Observed": item.observed_date,
                    "Confidence": item.evidence_confidence,
                    "Shouldn't be true": item.things_that_shouldnt_be_true,
                    "Tags": ", ".join(item.tags),
                }
                for item in opportunities
            ],
            hide_index=True,
            use_container_width=True,
        )
        convertible = [
            item for item in opportunities if item.status != "Converted to product candidate"
        ]
        if convertible:
            with st.form("convert_opportunity"):
                options = {f"#{item.id} · {item.title}": item.id for item in convertible}
                selected = st.selectbox("Opportunity to convert", options)
                st.caption("Conversion creates a product candidate and preserves the vault record.")
                if st.form_submit_button("Convert to product candidate", type="primary"):
                    try:
                        product = convert_opportunity_to_product(session, options[selected], "user")
                        session.commit()
                        st.success(f"Created product #{product.id}: {product.name}")
                        st.rerun()
                    except ValueError as exc:
                        session.rollback()
                        st.error(str(exc))


def product_pipeline(session: Session) -> None:
    page_header(
        "Product pipeline", "Capture opportunities manually or import a reviewable CSV batch."
    )
    intake, csv_tab, pipeline = st.tabs(["New product", "CSV import", "Pipeline"])
    with intake:
        with st.form("product_intake", clear_on_submit=True):
            left, right = st.columns(2)
            name = left.text_input("Product name *")
            url = left.text_input("Product URL")
            source = left.text_input("Source platform")
            category = left.text_input("Category")
            target = right.text_area("Target customer")
            problem = right.text_area("Customer problem or desire")
            st.subheader("Editable assumptions")
            money_fields = st.columns(4)
            price = money_fields[0].number_input("Selling price", min_value=0.0, step=0.01)
            product_cost = money_fields[1].number_input("Product cost", min_value=0.0, step=0.01)
            shipping = money_fields[2].number_input("Shipping cost", min_value=0.0, step=0.01)
            packaging = money_fields[3].number_input("Packaging cost", min_value=0.0, step=0.01)
            cost_fields = st.columns(4)
            processing = cost_fields[0].number_input("Payment processing", min_value=0.0, step=0.01)
            refund = cost_fields[1].number_input("Refund allowance", min_value=0.0, step=0.01)
            cac = cost_fields[2].number_input("Estimated CAC", min_value=0.0, step=0.01)
            platform = cost_fields[3].number_input("Platform allocation", min_value=0.0, step=0.01)
            supplier = left.text_input("Supplier")
            supplier_location = right.text_input("Supplier location")
            shipping_time = left.text_input("Shipping time")
            moq = right.number_input("Minimum order quantity", min_value=0, step=1)
            marketplace = st.text_area("Marketplace evidence")
            search = st.text_area("Search evidence")
            social = st.text_area("Social evidence")
            competition = st.text_area("Competition notes")
            complaints = st.text_area("Review complaints")
            upsells = st.text_area("Upsell ideas")
            repeat = st.text_area("Repeat-purchase potential")
            fulfillment = st.text_area("Fulfillment risk")
            legal = st.text_area("Legal or policy concerns")
            research = st.text_area("Research notes")
            submitted = st.form_submit_button("Save opportunity", type="primary")
        if submitted:
            try:
                data = ProductCreate(
                    name=name,
                    product_url=url or None,
                    source_platform=source or None,
                    category=category or None,
                    target_customer=target or None,
                    customer_problem=problem or None,
                    proposed_selling_price=Decimal(str(price)),
                    product_cost=Decimal(str(product_cost)),
                    shipping_cost=Decimal(str(shipping)),
                    packaging_cost=Decimal(str(packaging)),
                    payment_processing_estimate=Decimal(str(processing)),
                    expected_refund_allowance=Decimal(str(refund)),
                    estimated_cac=Decimal(str(cac)),
                    platform_cost_allocation=Decimal(str(platform)),
                    supplier=supplier or None,
                    supplier_location=supplier_location or None,
                    shipping_time=shipping_time or None,
                    minimum_order_quantity=moq,
                    marketplace_evidence=marketplace or None,
                    search_evidence=search or None,
                    social_evidence=social or None,
                    competition_notes=competition or None,
                    review_complaints=complaints or None,
                    upsell_ideas=upsells or None,
                    repeat_purchase_potential=repeat or None,
                    fulfillment_risk=fulfillment or None,
                    legal_policy_concerns=legal or None,
                    research_notes=research or None,
                )
                product = create_product(session, data)
                session.commit()
                st.success(f"Saved {product.name} as Discovered.")
            except (ValidationError, ValueError) as exc:
                session.rollback()
                st.error(str(exc))
    with csv_tab:
        st.caption("Required column: name. Other ProductCreate field names are optional.")
        upload = st.file_uploader("Product CSV", type=["csv"])
        if upload:
            frame = pd.read_csv(upload).fillna("")
            st.dataframe(frame.head(25), use_container_width=True)
            if st.button("Import reviewed rows", type="primary"):
                rows: list[dict[str, Any]] = [
                    {str(key): value for key, value in row.items()}
                    for row in frame.to_dict(orient="records")
                ]
                count, errors = import_products(session, rows, "user")
                session.commit()
                st.success(f"Imported {count} products.")
                if errors:
                    st.warning("\n".join(errors))
    with pipeline:
        products = list_products(session)
        st.dataframe(
            [
                {
                    "ID": p.id,
                    "Product": p.name,
                    "Category": p.category,
                    "Status": p.status,
                    "Price": float(p.proposed_selling_price),
                    "Fictional": p.is_fictional,
                }
                for p in products
            ],
            use_container_width=True,
            hide_index=True,
        )


def ranked_opportunities(session: Session) -> None:
    page_header(
        "Ranked opportunities",
        "Latest explainable score for each product; penalties remain visible.",
    )
    snapshots = list(
        session.scalars(select(ScoreSnapshot).order_by(ScoreSnapshot.created_at.desc()))
    )
    latest: dict[int, ScoreSnapshot] = {}
    for item in snapshots:
        latest.setdefault(item.product_id, item)
    if latest:
        rows = []
        for product_id, score in latest.items():
            product = session.get(Product, product_id)
            rows.append(
                {
                    "Product": product.name if product else product_id,
                    "Base": float(score.base_score),
                    "Penalties": float(score.penalty_total),
                    "Final": float(score.final_score),
                }
            )
        st.dataframe(
            pd.DataFrame(rows).sort_values("Final", ascending=False),
            hide_index=True,
            use_container_width=True,
        )
    else:
        empty_state("No score snapshots yet.")
    product = _selected_product(session, "score_product")
    if not product:
        return
    with st.form("score_form"):
        active_weights = get_scoring_weights(session)
        st.caption(
            "Active weights: "
            + ", ".join(
                f"{name.replace('_', ' ')} {weight * 100}%"
                for name, weight in active_weights.items()
            )
        )
        st.subheader("Components (0-100)")
        components = {
            name: Decimal(str(st.slider(name.replace("_", " ").title(), 0, 100, 50)))
            for name in DEFAULT_WEIGHTS
        }
        st.subheader("Risk penalties (0-10 each)")
        penalties = {
            name: Decimal(str(st.slider(name.replace("_", " ").title(), 0, 10, 0)))
            for name in PENALTY_FIELDS
        }
        rationale = st.text_area("Rationale and evidence references")
        if st.form_submit_button("Save score snapshot", type="primary"):
            saved = save_score(
                session,
                product_id=product.id,
                components=components,
                penalties=penalties,
                actor="user",
                rationale=rationale,
                weights=active_weights,
            )
            session.commit()
            st.success(f"Saved explainable score {saved.final_score}.")


def product_detail(session: Session) -> None:
    page_header("Product detail", "Research record and controlled decision movement.")
    product = _selected_product(session, "detail_product")
    if not product:
        return
    st.subheader(product.name)
    st.write(
        {
            "status": product.status,
            "category": product.category,
            "supplier": product.supplier,
            "source_platform": product.source_platform,
            "created_at": product.created_at,
        }
    )
    st.markdown("**Customer and research context**")
    st.write(product.customer_problem or "Not recorded")
    edit_tab, history_tab, decision_tab = st.tabs(
        ["Edit current version", "Version history", "Pipeline decision"]
    )
    with edit_tab, st.form("product_edit_form"):
        st.caption(f"Editing version {product.current_version}. Saving creates a new version.")
        columns = st.columns(2)
        name = columns[0].text_input("Product name", value=product.name)
        category = columns[1].text_input("Category", value=product.category or "")
        target_customer = columns[0].text_area(
            "Target customer", value=product.target_customer or ""
        )
        customer_problem = columns[1].text_area(
            "Problem or desire", value=product.customer_problem or ""
        )
        source_platform = columns[0].text_input(
            "Source platform", value=product.source_platform or ""
        )
        product_url = columns[1].text_input("Product URL", value=product.product_url or "")
        st.markdown("**Financial assumptions**")
        money_columns = st.columns(5)
        financial_inputs = {
            "proposed_selling_price": money_columns[0].number_input(
                "Selling price", value=float(product.proposed_selling_price), min_value=0.0
            ),
            "product_cost": money_columns[1].number_input(
                "Product cost", value=float(product.product_cost), min_value=0.0
            ),
            "shipping_cost": money_columns[2].number_input(
                "Shipping", value=float(product.shipping_cost), min_value=0.0
            ),
            "packaging_cost": money_columns[3].number_input(
                "Packaging", value=float(product.packaging_cost), min_value=0.0
            ),
            "estimated_cac": money_columns[4].number_input(
                "Estimated CAC", value=float(product.estimated_cac), min_value=0.0
            ),
            "payment_processing_estimate": money_columns[0].number_input(
                "Payment processing",
                value=float(product.payment_processing_estimate),
                min_value=0.0,
            ),
            "expected_refund_allowance": money_columns[1].number_input(
                "Refund allowance",
                value=float(product.expected_refund_allowance),
                min_value=0.0,
            ),
            "platform_cost_allocation": money_columns[2].number_input(
                "Platform allocation",
                value=float(product.platform_cost_allocation),
                min_value=0.0,
            ),
            "chargeback_allowance": money_columns[3].number_input(
                "Chargeback allowance",
                value=float(product.chargeback_allowance),
                min_value=0.0,
            ),
            "discount_estimate": money_columns[4].number_input(
                "Discount estimate", value=float(product.discount_estimate), min_value=0.0
            ),
        }
        research_notes = st.text_area("Research notes", value=product.research_notes or "")
        reason = st.text_area("Reason for change *")
        metadata = st.columns(3)
        provenance = metadata[0].selectbox(
            "Value type", ["Observed", "Estimated", "Inferred", "User-entered"]
        )
        source = metadata[1].text_input("Source")
        support = metadata[2].text_input("Supporting evidence")
        if st.form_submit_button("Save as new version", type="primary"):
            proposed: dict[str, Any] = {
                "name": name,
                "category": category or None,
                "target_customer": target_customer or None,
                "customer_problem": customer_problem or None,
                "source_platform": source_platform or None,
                "product_url": product_url or None,
                "research_notes": research_notes or None,
                **{key: Decimal(str(value)) for key, value in financial_inputs.items()},
            }
            current = {key: getattr(product, key) for key in proposed}
            changes = {
                key: value
                for key, value in proposed.items()
                if str(current[key] or "") != str(value or "")
            }
            try:
                edit_product(
                    session,
                    ProductEdit(
                        product_id=product.id,
                        based_on_version=product.current_version,
                        changes=changes,
                        actor="user",
                        reason=reason,
                        source=source or None,
                        supporting_evidence=support or None,
                        provenance=provenance,
                    ),
                )
                session.commit()
                st.success("Product updated as a new historical version.")
                st.rerun()
            except (ValidationError, ValueError) as exc:
                session.rollback()
                st.error(str(exc))
    with history_tab:
        versions = list(
            session.scalars(
                select(ProductVersion)
                .where(ProductVersion.product_id == product.id)
                .order_by(ProductVersion.version_number.desc())
            )
        )
        st.dataframe(
            [
                {
                    "Version": item.version_number,
                    "Created": item.created_at,
                    "Actor": item.actor,
                    "Reason": item.reason,
                    "Source": item.source,
                    "Value type": item.provenance,
                }
                for item in versions
            ],
            hide_index=True,
            use_container_width=True,
        )
        if len(versions) >= 2:
            version_numbers = [item.version_number for item in versions]
            compare_columns = st.columns(2)
            left_number = compare_columns[0].selectbox(
                "Earlier version", version_numbers, index=len(version_numbers) - 1
            )
            right_number = compare_columns[1].selectbox("Later version", version_numbers, index=0)
            by_number = {item.version_number: item for item in versions}
            left_snapshot = by_number[left_number].snapshot
            right_snapshot = by_number[right_number].snapshot
            comparison = [
                {
                    "Field": field,
                    f"v{left_number}": left_snapshot.get(field),
                    f"v{right_number}": right_snapshot.get(field),
                }
                for field in sorted(left_snapshot)
                if left_snapshot.get(field) != right_snapshot.get(field)
            ]
            st.dataframe(comparison, hide_index=True, use_container_width=True)
        with st.form("rollback_form"):
            target = st.selectbox(
                "Restore values from version", [v.version_number for v in versions]
            )
            rollback_reason = st.text_input("Rollback reason")
            if st.form_submit_button("Create restorative version"):
                try:
                    rollback_product(
                        session,
                        product_id=product.id,
                        target_version=target,
                        based_on_version=product.current_version,
                        actor="user",
                        reason=rollback_reason,
                    )
                    session.commit()
                    st.success("Values restored in a new version; history was preserved.")
                    st.rerun()
                except (ValidationError, ValueError) as exc:
                    session.rollback()
                    st.error(str(exc))
    with decision_tab, st.form("status_form"):
        new_status = st.selectbox(
            "New status", [x for x in PIPELINE_STATUSES if x != product.status]
        )
        reason = st.text_area("Reason *")
        supporting = st.text_area("Supporting evidence")
        next_action = st.text_input("Next action")
        if st.form_submit_button("Record status change", type="primary"):
            try:
                change_status(
                    session,
                    StatusChange(
                        product_id=product.id,
                        new_status=new_status,
                        reason=reason,
                        actor="user",
                        supporting_evidence=supporting or None,
                        next_action=next_action or None,
                    ),
                )
                session.commit()
                st.success("Status change recorded and audited.")
            except (ValidationError, ValueError) as exc:
                session.rollback()
                st.error(str(exc))


def unit_economics(session: Session) -> None:
    page_header("Unit economics", "Editable assumptions with transparent break-even calculations.")
    product = _selected_product(session, "economics_product")
    if not product:
        return
    with st.form("economics_form"):
        fields = st.columns(3)
        price = fields[0].number_input(
            "Gross revenue", value=float(product.proposed_selling_price), min_value=0.0
        )
        discount = fields[1].number_input(
            "Discounts", value=float(product.discount_estimate), min_value=0.0
        )
        cost = fields[2].number_input(
            "Product cost", value=float(product.product_cost), min_value=0.0
        )
        shipping = fields[0].number_input(
            "Shipping", value=float(product.shipping_cost), min_value=0.0
        )
        packaging = fields[1].number_input(
            "Packaging", value=float(product.packaging_cost), min_value=0.0
        )
        processing = fields[2].number_input(
            "Payment processing", value=float(product.payment_processing_estimate), min_value=0.0
        )
        platform = fields[0].number_input(
            "Platform allocation", value=float(product.platform_cost_allocation), min_value=0.0
        )
        refunds = fields[1].number_input(
            "Refund allowance", value=float(product.expected_refund_allowance), min_value=0.0
        )
        chargebacks = fields[2].number_input(
            "Chargeback allowance", value=float(product.chargeback_allowance), min_value=0.0
        )
        cac = fields[0].number_input(
            "Customer acquisition cost", value=float(product.estimated_cac), min_value=0.0
        )
        calculate = st.form_submit_button("Calculate", type="primary")
    if calculate:
        values = [
            price,
            discount,
            cost,
            shipping,
            packaging,
            processing,
            platform,
            refunds,
            chargebacks,
            cac,
        ]
        result = calculate_unit_economics(EconomicsInputs(*[Decimal(str(x)) for x in values]))
        metrics = st.columns(4)
        metrics[0].metric("Contribution margin", money_label(result.contribution_margin))
        metrics[1].metric("Margin %", f"{result.contribution_margin_percentage}%")
        metrics[2].metric("Break-even CAC", money_label(result.break_even_cac))
        metrics[3].metric("Break-even ROAS", str(result.break_even_roas or "N/A"))
        st.dataframe(
            [
                {"Orders": volume, "Estimated profit": float(profit)}
                for volume, profit in result.profit_by_volume.items()
            ],
            hide_index=True,
        )


def evidence_timeline(session: Session) -> None:
    page_header(
        "Evidence timeline",
        "Append-only observations with provenance, collection method, and confidence.",
    )
    product = _selected_product(session, "evidence_product")
    if not product:
        return
    with st.form("evidence_form", clear_on_submit=True):
        cols = st.columns(2)
        evidence_type = cols[0].text_input("Evidence type *")
        source = cols[1].text_input("Source *")
        source_url = cols[0].text_input("Source URL")
        observation = st.text_area("Observation *")
        numeric = cols[0].number_input("Numeric value (optional)", value=None)
        unit = cols[1].text_input("Unit")
        geography = cols[0].text_input("Geography")
        period = cols[1].text_input("Time period")
        method = cols[0].text_input("Collection method *", value="Manual research")
        confidence = cols[1].selectbox("Confidence", ["Low", "Medium", "High"])
        provenance = cols[0].selectbox(
            "Record type", ["Observed", "Estimated", "Inferred", "User-entered"]
        )
        notes = st.text_area("Notes")
        if st.form_submit_button("Append evidence", type="primary"):
            try:
                append_evidence(
                    session,
                    EvidenceCreate(
                        product_id=product.id,
                        evidence_type=evidence_type,
                        source=source,
                        source_url=source_url or None,
                        observation=observation,
                        numeric_value=Decimal(str(numeric)) if numeric is not None else None,
                        unit=unit or None,
                        geography=geography or None,
                        time_period=period or None,
                        collected_at=datetime.now(UTC),
                        collection_method=method,
                        confidence_level=confidence,
                        provenance=provenance,
                        notes=notes or None,
                    ),
                )
                session.commit()
                st.success("Evidence appended. Historical records are never edited here.")
            except (ValidationError, ValueError) as exc:
                session.rollback()
                st.error(str(exc))
    records = list(
        session.scalars(
            select(Evidence)
            .where(Evidence.product_id == product.id)
            .order_by(Evidence.collected_at.desc())
        )
    )
    st.dataframe(
        [
            {
                "Collected": e.collected_at,
                "Type": e.evidence_type,
                "Source": e.source,
                "Observation": e.observation,
                "Value": e.numeric_value,
                "Unit": e.unit,
                "Confidence": e.confidence_level,
                "Record type": e.provenance,
            }
            for e in records
        ],
        hide_index=True,
        use_container_width=True,
    )


def research_workbench(session: Session) -> None:
    page_header(
        "Research Workbench",
        "Complete guided diligence and link every important conclusion to stored evidence.",
    )
    product = _selected_product(session, "research_product")
    if not product:
        return
    assessment = assess_research(session, product.id)
    columns = st.columns(3)
    columns[0].metric(
        "Research completeness",
        f"{assessment.completeness_percentage}%",
        help="Share of the 22 research sections with a current saved entry.",
    )
    columns[1].metric(
        "Evidence-linked gaps",
        len(assessment.unsupported_sections),
        help="Completed conclusions with no linked internal evidence record.",
    )
    columns[2].metric(
        "Unsupported score components",
        len(assessment.unsupported_score_components),
        help="Score components lacking an evidence-linked research section.",
    )
    st.progress(float(assessment.completeness_percentage / 100))
    if assessment.enough_evidence:
        st.success("Evidence threshold met for recommendation review—not proof of viability.")
    else:
        st.error("Not enough evidence for a responsible recommendation.")
    alert_tabs = st.tabs(["Missing", "Unsupported", "Stale / contradictory", "Score gaps"])
    with alert_tabs[0]:
        st.write(assessment.missing_sections or "No missing sections.")
        if assessment.missing_critical_sections:
            st.warning("Critical: " + ", ".join(assessment.missing_critical_sections))
    with alert_tabs[1]:
        st.write(assessment.unsupported_sections or "No unsupported completed sections.")
    with alert_tabs[2]:
        st.write(
            {
                "stale_evidence_ids": assessment.stale_evidence_ids,
                "contradictory_groups": assessment.contradictory_evidence_groups,
            }
        )
    with alert_tabs[3]:
        st.write(assessment.unsupported_score_components or "Every score component has support.")

    latest = latest_research_entries(session, product.id)
    evidence_records = list(
        session.scalars(
            select(Evidence)
            .where(Evidence.product_id == product.id)
            .order_by(Evidence.collected_at.desc())
        )
    )
    evidence_options = {
        f"#{item.id} · {item.evidence_type} · {item.source}": item.id for item in evidence_records
    }
    with st.form("research_entry_form"):
        section_key = st.selectbox(
            "Research section",
            RESEARCH_SECTIONS,
            format_func=lambda key: RESEARCH_SECTIONS[key],
        )
        current_entry = latest.get(section_key)
        content = st.text_area(
            "Current conclusion or finding",
            value=current_entry.content if current_entry else "",
            height=180,
        )
        selected_evidence = st.multiselect("Supporting evidence records", evidence_options)
        provenance = st.selectbox(
            "Conclusion type", ["Observed", "Estimated", "Inferred", "User-entered"]
        )
        reason = st.text_input("Reason for this research version")
        if st.form_submit_button("Save research version", type="primary"):
            try:
                save_research_entry(
                    session,
                    product_id=product.id,
                    section_key=section_key,
                    content=content,
                    evidence_ids=[evidence_options[label] for label in selected_evidence],
                    provenance=provenance,
                    actor="user",
                    reason=reason,
                )
                session.commit()
                st.success("Research version saved and audited.")
                st.rerun()
            except ValueError as exc:
                session.rollback()
                st.error(str(exc))
    markdown_report, json_report = export_research_report(session, product.id)
    downloads = st.columns(2)
    downloads[0].download_button(
        "Export Markdown report",
        markdown_report,
        file_name=f"product-{product.id}-research.md",
        mime="text/markdown",
    )
    downloads[1].download_button(
        "Export JSON report",
        json_report,
        file_name=f"product-{product.id}-research.json",
        mime="application/json",
    )


def supplier_comparison(session: Session) -> None:
    page_header(
        "Supplier comparison", "Compare offers without initiating supplier contact or orders."
    )
    product = _selected_product(session, "supplier_product")
    if not product:
        return
    with st.form("supplier_form", clear_on_submit=True):
        cols = st.columns(3)
        name = cols[0].text_input("Supplier name *")
        location = cols[1].text_input("Location")
        quality = cols[2].selectbox("Evidence quality", ["Low", "Medium", "High"])
        unit_cost = cols[0].number_input("Unit cost", min_value=0.0)
        shipping = cols[1].number_input("Shipping cost", min_value=0.0)
        lead = cols[2].number_input("Lead time days", min_value=0, step=1)
        moq = cols[0].number_input("MOQ", min_value=0, step=1)
        notes = st.text_area("Notes")
        if st.form_submit_button("Add supplier offer", type="primary"):
            if not name.strip():
                st.error("Supplier name is required.")
            else:
                offer = SupplierOffer(
                    product_id=product.id,
                    supplier_name=name,
                    location=location or None,
                    unit_cost=Decimal(str(unit_cost)),
                    shipping_cost=Decimal(str(shipping)),
                    lead_time_days=lead,
                    minimum_order_quantity=moq,
                    evidence_quality=quality,
                    notes=notes or None,
                )
                session.add(offer)
                session.flush()
                record_audit(
                    session,
                    event_type="data_change",
                    entity_type="supplier_offer",
                    entity_id=offer.id,
                    actor="user",
                    action="create",
                )
                session.commit()
                st.success("Supplier offer recorded.")
    offers = list(
        session.scalars(select(SupplierOffer).where(SupplierOffer.product_id == product.id))
    )
    st.dataframe(
        [
            {
                "Supplier": x.supplier_name,
                "Location": x.location,
                "Unit cost": float(x.unit_cost),
                "Shipping": float(x.shipping_cost),
                "Lead days": x.lead_time_days,
                "MOQ": x.minimum_order_quantity,
                "Evidence": x.evidence_quality,
            }
            for x in offers
        ],
        hide_index=True,
        use_container_width=True,
    )


def recommendation_brief(session: Session) -> None:
    page_header(
        "Recommendation Brief",
        "A deterministic, evidence-citing decision aid that never authorizes action.",
    )
    product = _selected_product(session, "recommendation_product")
    if not product:
        return
    brief = DeterministicRecommendationGenerator().generate(session, product.id)
    metrics = st.columns(4)
    metrics[0].metric("Recommendation", brief.recommendation.title())
    metrics[1].metric("Confidence", brief.confidence_level)
    metrics[2].metric("Evidence completeness", f"{brief.evidence_completeness}%")
    metrics[3].metric(
        "Validation budget ceiling",
        money_label(brief.maximum_validation_budget),
        help="The lower of $500 or ten break-even acquisitions; zero until evidence gates pass.",
    )
    st.warning(brief.certainty_notice)
    columns = st.columns(2)
    with columns[0]:
        st.subheader("Reasons in favor")
        st.write(brief.primary_reasons_in_favor)
        st.subheader("Critical unknowns")
        st.write(brief.critical_unknowns)
    with columns[1]:
        st.subheader("Reasons against")
        st.write(brief.primary_reasons_against)
        st.subheader("Conditions that reverse this recommendation")
        st.write(brief.reversal_conditions)
    st.subheader("Unit economics")
    st.write(brief.unit_economics_summary)
    st.write(
        {
            "break_even_cac": brief.break_even_cac,
            "break_even_roas": brief.break_even_roas,
            "suggested_next_experiment": brief.suggested_next_experiment,
        }
    )
    st.subheader("Internal evidence cited")
    st.write(brief.evidence_citations or ["No internal evidence records are available."])
    markdown = render_recommendation_markdown(brief)
    json_report = render_recommendation_json(brief)
    downloads = st.columns(2)
    downloads[0].download_button(
        "Export brief as Markdown",
        markdown,
        file_name=f"product-{product.id}-recommendation.md",
        mime="text/markdown",
    )
    downloads[1].download_button(
        "Export brief as JSON",
        json_report,
        file_name=f"product-{product.id}-recommendation.json",
        mime="application/json",
    )


def validation_experiments(session: Session) -> None:
    page_header(
        "Validation experiments",
        "Plan and record capped tests. No advertising or spending is automated.",
    )
    product = _selected_product(session, "experiment_product")
    if not product:
        return
    with st.form("experiment_form", clear_on_submit=True):
        hypothesis = st.text_area("Hypothesis *")
        cols = st.columns(3)
        test_type = cols[0].text_input("Test type *")
        audience = cols[1].text_input("Audience")
        channel = cols[2].text_input("Channel")
        offer = st.text_area("Offer")
        creative = st.text_area("Creative")
        price = cols[0].number_input("Price", min_value=0.0)
        budget = cols[1].number_input("Budget ceiling", min_value=0.0)
        start_date = cols[0].date_input("Start date", value=None)
        end_date = cols[1].date_input("End date", value=None)
        visits = cols[0].number_input("Visits", min_value=0, step=1)
        signups = cols[1].number_input("Email signups", min_value=0, step=1)
        carts = cols[2].number_input("Add to carts", min_value=0, step=1)
        checkouts = cols[0].number_input("Checkout initiations", min_value=0, step=1)
        purchases = cols[1].number_input("Purchases", min_value=0, step=1)
        revenue = cols[2].number_input("Revenue", min_value=0.0)
        refunds = cols[0].number_input("Refunds", min_value=0.0)
        cost = cols[1].number_input("Test cost", min_value=0.0)
        result = st.text_area("Result")
        lessons = st.text_area("Lessons")
        decision = st.selectbox("Decision", ["Pending", "Fail", "Iterate", "Pass"])
        if st.form_submit_button("Save experiment", type="primary"):
            if not hypothesis.strip() or not test_type.strip():
                st.error("Hypothesis and test type are required.")
            else:
                metrics = derived_experiment_metrics(
                    visits=visits,
                    purchases=purchases,
                    cost=Decimal(str(cost)),
                    revenue=Decimal(str(revenue)),
                    refunds=Decimal(str(refunds)),
                )
                experiment = ValidationExperiment(
                    product_id=product.id,
                    hypothesis=hypothesis,
                    test_type=test_type,
                    audience=audience or None,
                    channel=channel or None,
                    offer=offer or None,
                    creative=creative or None,
                    price=Decimal(str(price)),
                    budget_ceiling=Decimal(str(budget)),
                    start_date=start_date,
                    end_date=end_date,
                    visits=visits,
                    email_signups=signups,
                    add_to_carts=carts,
                    checkout_initiations=checkouts,
                    purchases=purchases,
                    revenue=Decimal(str(revenue)),
                    refunds=Decimal(str(refunds)),
                    cost=Decimal(str(cost)),
                    result=result or None,
                    lessons=lessons or None,
                    decision=decision,
                    **metrics,
                )
                session.add(experiment)
                session.flush()
                record_audit(
                    session,
                    event_type="data_change",
                    entity_type="validation_experiment",
                    entity_id=experiment.id,
                    actor="user",
                    action="create",
                )
                session.commit()
                st.success("Experiment recorded.")
    experiments = list(
        session.scalars(
            select(ValidationExperiment).where(ValidationExperiment.product_id == product.id)
        )
    )
    st.dataframe(
        [
            {
                "Hypothesis": x.hypothesis,
                "Test": x.test_type,
                "Visits": x.visits,
                "Purchases": x.purchases,
                "Conversion %": float(x.conversion_rate),
                "CAC": float(x.customer_acquisition_cost),
                "Contribution profit": float(x.contribution_profit),
                "Decision": x.decision,
            }
            for x in experiments
        ],
        hide_index=True,
        use_container_width=True,
    )


def decision_history(session: Session) -> None:
    page_header("Decision history", "Chronological, reasoned product status decisions.")
    records = list(session.scalars(select(StatusHistory).order_by(StatusHistory.changed_at.desc())))
    st.dataframe(
        [
            {
                "Time": x.changed_at,
                "Product ID": x.product_id,
                "From": x.previous_status,
                "To": x.new_status,
                "Reason": x.reason,
                "Actor": x.actor,
                "Evidence": x.supporting_evidence,
                "Next action": x.next_action,
            }
            for x in records
        ],
        hide_index=True,
        use_container_width=True,
    )


def risks_warnings(session: Session) -> None:
    page_header("Risks and warnings", "Visible research flags requiring human review.")
    products = list_products(session)
    rows: list[dict[str, Any]] = []
    for product in products:
        for kind, value in (
            ("Fulfillment", product.fulfillment_risk),
            ("Legal / policy", product.legal_policy_concerns),
            ("Review complaints", product.review_complaints),
        ):
            if value:
                rows.append(
                    {
                        "Product": product.name,
                        "Risk type": kind,
                        "Details": value,
                        "Status": product.status,
                    }
                )
    if rows:
        st.dataframe(rows, hide_index=True, use_container_width=True)
    else:
        empty_state("No explicit risk notes recorded. Absence of a flag is not evidence of safety.")


def system_settings(session: Session) -> None:
    page_header("System settings", "Inspect assumptions and the audit trail.")
    weights, audit = st.tabs(["Scoring weights", "Audit log"])
    with weights:
        active_weights = get_scoring_weights(session)
        st.dataframe(
            [{"Component": k, "Weight %": float(v * 100)} for k, v in active_weights.items()],
            hide_index=True,
        )
        with st.form("weight_settings"):
            entered = {
                name: Decimal(
                    str(
                        st.number_input(
                            name.replace("_", " ").title(),
                            min_value=0.0,
                            max_value=100.0,
                            value=float(active_weights[name] * 100),
                            step=1.0,
                        )
                    )
                )
                / Decimal("100")
                for name in DEFAULT_WEIGHTS
            }
            st.caption(f"Entered total: {sum(entered.values(), start=Decimal('0')) * 100}%")
            if st.form_submit_button("Save scoring weights", type="primary"):
                try:
                    save_scoring_weights(session, entered, "user")
                    session.commit()
                    st.success("Scoring weights saved and audited.")
                except ValueError as exc:
                    session.rollback()
                    st.error(str(exc))
    with audit:
        logs = list(
            session.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(500))
        )
        st.dataframe(
            [
                {
                    "Time": x.created_at,
                    "Event": x.event_type,
                    "Entity": x.entity_type,
                    "ID": x.entity_id,
                    "Actor": x.actor,
                    "Action": x.action,
                    "Details": x.details,
                }
                for x in logs
            ],
            hide_index=True,
            use_container_width=True,
        )


PAGES = {
    "Executive overview": executive_overview,
    "Opportunity Vault": opportunity_vault,
    "Product pipeline": product_pipeline,
    "Ranked opportunities": ranked_opportunities,
    "Product detail": product_detail,
    "Unit economics": unit_economics,
    "Evidence timeline": evidence_timeline,
    "Research Workbench": research_workbench,
    "Recommendation Brief": recommendation_brief,
    "Supplier comparison": supplier_comparison,
    "Validation experiments": validation_experiments,
    "Decision history": decision_history,
    "Risks and warnings": risks_warnings,
    "System settings": system_settings,
}
