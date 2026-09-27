# ============================================================
# AEGIE DATA ANALYST REFERENCE KNOWLEDGE
# ============================================================
#
# Reference concepts for the 12 Data Analyst questions.
#
# IMPORTANT:
# - These are NOT participant answers.
# - These are NOT primary dataset samples.
# - They are development-stage semantic reference resources.
# - reference_answer supports whole-answer and sentence-level comparison.
# - key_concepts support concept-level evidence.
# - Expert review is required before the final study.
# ============================================================


DATA_ANALYST_REFERENCES = {

    # ========================================================
    # EASY
    # ========================================================

    "DA_E01": {
        "question": (
            "What is the difference between mean and median?"
        ),
        "reference_answer": (
            "The mean is calculated by adding all values and dividing by the number "
            "of values, while the median is the middle value after the data is arranged "
            "in order. The mean can be strongly affected by extreme values or outliers, "
            "whereas the median is generally more resistant to extreme values."
        ),
        "key_concepts": [
            "Mean is calculated by adding all values and dividing by the number of values.",
            "Median is the middle value after the data is arranged in order.",
            "Mean can be strongly affected by extreme values or outliers.",
            "Median is generally more resistant to extreme values than the mean."
        ],
        "acceptable_examples": [
            "For 2, 4, and 6, the mean and median are both 4.",
            "For highly skewed data such as income, the median can be more representative than the mean."
        ]
    },

    "DA_E02": {
        "question": (
            "What is a primary key in a database?"
        ),
        "reference_answer": (
            "A primary key is a column or combination of columns that uniquely "
            "identifies each row in a database table. Primary key values must be "
            "unique and cannot contain NULL values. Depending on the database design, "
            "a primary key can consist of one column or multiple columns."
        ),
        "key_concepts": [
            "A primary key uniquely identifies each row in a database table.",
            "Primary key values must be unique within the table.",
            "A primary key cannot contain NULL values.",
            "A primary key can consist of one column or a combination of columns depending on the database design."
        ],
        "acceptable_examples": [
            "customer_id can be used as the primary key of a customer table.",
            "A composite primary key can use multiple columns to uniquely identify a row."
        ]
    },

    "DA_E03": {
        "question": (
            "What is the purpose of data visualization?"
        ),
        "reference_answer": (
            "Data visualization represents data using graphical forms such as charts "
            "and plots. It helps people understand patterns, trends, relationships, "
            "and distributions and can also reveal unusual values or possible outliers. "
            "Visualization is also useful for communicating analytical findings to both "
            "technical and nontechnical audiences."
        ),
        "key_concepts": [
            "Data visualization represents data using graphical forms such as charts and plots.",
            "Visualization helps people understand patterns, trends, relationships, and distributions.",
            "It can help identify unusual values or potential outliers.",
            "Visualization supports communication of analytical findings to technical and nontechnical audiences."
        ],
        "acceptable_examples": [
            "A line chart can show how sales change over time.",
            "A bar chart can compare values across categories."
        ]
    },

    "DA_E04": {
        "question": (
            "What is the difference between structured and unstructured data?"
        ),
        "reference_answer": (
            "Structured data follows a predefined and organized schema and is commonly "
            "represented using rows, columns, and defined fields. Unstructured data does "
            "not naturally follow a fixed tabular schema. Free text, images, audio, and "
            "video are common examples of unstructured data."
        ),
        "key_concepts": [
            "Structured data follows a predefined and organized schema.",
            "Structured data is commonly represented using rows, columns, and defined fields.",
            "Unstructured data does not naturally follow a fixed tabular schema.",
            "Examples of unstructured data can include free text, images, audio, and video."
        ],
        "acceptable_examples": [
            "A relational database table is structured data.",
            "Customer review text and images are examples of unstructured data."
        ]
    },


    # ========================================================
    # MEDIUM
    # ========================================================

    "DA_M01": {
        "question": (
            "How would you handle missing values in a dataset?"
        ),
        "reference_answer": (
            "Before handling missing values, the amount, pattern, and possible cause "
            "of the missing data should be investigated. Depending on the situation, "
            "rows or columns may be removed, or missing values may be imputed using "
            "suitable statistical or model-based methods. The treatment should consider "
            "the data type, analysis objective, missingness mechanism, and the risk of "
            "introducing bias."
        ),
        "key_concepts": [
            "The amount, pattern, and possible cause of missing data should be investigated before choosing a treatment.",
            "Rows or columns can sometimes be removed when missingness is limited and removal is justified.",
            "Missing values can be imputed using suitable statistical or model-based methods.",
            "The treatment should consider the data type, analysis objective, missingness mechanism, and risk of introducing bias."
        ],
        "acceptable_examples": [
            "A numerical variable may be imputed using the median when appropriate.",
            "A categorical variable may use an appropriate category or imputation strategy.",
            "A column with excessive unusable missing data may sometimes be removed."
        ]
    },

    "DA_M02": {
        "question": (
            "Explain the difference between WHERE and HAVING in SQL."
        ),
        "reference_answer": (
            "WHERE and HAVING both filter data in SQL, but they operate at different "
            "stages. WHERE filters individual rows before grouping and aggregation, "
            "while HAVING filters groups or aggregated results after grouping. HAVING "
            "is therefore commonly used with GROUP BY and aggregate conditions."
        ),
        "key_concepts": [
            "WHERE filters rows before grouping and aggregation.",
            "HAVING filters groups or aggregated results after grouping.",
            "WHERE is commonly used for conditions on individual rows.",
            "HAVING is commonly used with GROUP BY and aggregate conditions."
        ],
        "acceptable_examples": [
            "WHERE salary > 50000 filters individual rows.",
            "HAVING COUNT(*) > 10 can retain groups containing more than ten rows."
        ]
    },

    "DA_M03": {
        "question": (
            "What is correlation and how is it different from causation?"
        ),
        "reference_answer": (
            "Correlation describes an association or statistical relationship between "
            "variables, while causation means that a change in one factor contributes "
            "to a change in another under an appropriate causal interpretation. "
            "Correlation alone does not establish causation. Confounding variables, "
            "reverse causality, selection effects, or coincidence can produce associations "
            "without the assumed causal relationship."
        ),
        "key_concepts": [
            "Correlation describes an association or statistical relationship between variables.",
            "Causation means that a change in one factor contributes to a change in another under an appropriate causal interpretation.",
            "Correlation alone does not establish causation.",
            "Confounding variables, reverse causality, selection effects, or coincidence can produce associations without the assumed causal relationship."
        ],
        "acceptable_examples": [
            "Two variables can increase together without one causing the other.",
            "A controlled experiment can provide stronger evidence for a causal effect when its assumptions are satisfied."
        ]
    },

    "DA_M04": {
        "question": (
            "How would you identify outliers in a dataset?"
        ),
        "reference_answer": (
            "Outliers are observations that are unusually different from the rest of "
            "the relevant data distribution. They can be identified using visual methods "
            "such as box plots or scatter plots and statistical approaches such as the "
            "interquartile range, z-scores, robust statistics, or domain-specific rules. "
            "An outlier should be investigated before deciding whether to remove, "
            "transform, correct, or retain it."
        ),
        "key_concepts": [
            "Outliers are observations that are unusually different from the rest of the relevant data distribution.",
            "Visual methods such as box plots or scatter plots can help identify unusual observations.",
            "Statistical approaches can include the interquartile range, z-scores, robust statistics, or domain-specific rules.",
            "An identified outlier should be investigated before deciding whether to remove, transform, correct, or retain it."
        ],
        "acceptable_examples": [
            "The IQR rule can flag values far below Q1 or above Q3.",
            "An extreme value may represent a data-entry error or a genuine rare event."
        ]
    },


    # ========================================================
    # HARD
    # ========================================================

    "DA_H01": {
        "question": (
            "How would you determine whether a change in a business metric is statistically significant?"
        ),
        "reference_answer": (
            "To determine whether a change in a business metric is statistically "
            "significant, first define a clear null hypothesis and alternative hypothesis. "
            "Then select an appropriate statistical test or confidence interval based on "
            "the metric, study design, data distribution, and assumptions. The observed "
            "effect size and uncertainty should also be evaluated rather than relying only "
            "on a p-value, and statistical significance should be distinguished from "
            "practical or business significance."
        ),
        "key_concepts": [
            "A clear null hypothesis and alternative hypothesis should be defined for the metric change.",
            "An appropriate statistical test or confidence interval should be selected based on the metric, study design, data distribution, and assumptions.",
            "The observed effect size and uncertainty should be evaluated rather than relying only on a p-value.",
            "Statistical significance should be distinguished from practical or business significance."
        ],
        "acceptable_examples": [
            "A confidence interval can quantify uncertainty around the estimated change.",
            "An A/B experiment may compare a conversion metric between treatment and control groups using an appropriate statistical method.",
            "A statistically detectable difference may still be too small to matter to the business."
        ]
    },

    "DA_H02": {
        "question": (
            "How would you analyze a dataset when two variables are highly correlated?"
        ),
        "reference_answer": (
            "When two variables are highly correlated, first examine the strength and "
            "nature of their relationship using suitable statistics and visualizations. "
            "High correlation does not by itself establish causation. If the variables "
            "are predictors, consider multicollinearity and its effect on coefficient "
            "stability or interpretation. Depending on the objective, the variables may "
            "be retained, removed, combined, transformed, regularized, or handled using "
            "dimensionality-reduction techniques."
        ),
        "key_concepts": [
            "The strength and nature of the relationship should first be examined using suitable statistics and visualizations.",
            "High correlation does not by itself establish a causal relationship.",
            "If the variables are predictors in a model, multicollinearity and its effect on coefficient stability or interpretation should be considered.",
            "Depending on the objective, variables may be retained, removed, combined, transformed, regularized, or handled using dimensionality-reduction techniques."
        ],
        "acceptable_examples": [
            "A correlation matrix and scatter plot can be used to inspect the relationship.",
            "Variance inflation factors can help diagnose multicollinearity in suitable regression settings.",
            "Regularization or feature selection may help when correlated predictors create modeling problems."
        ]
    },

    "DA_H03": {
        "question": (
            "How would you design an A/B test to evaluate a new product feature?"
        ),
        "reference_answer": (
            "To design an A/B test, first define a clear hypothesis and a primary outcome "
            "metric. Eligible experimental units should be assigned to control and treatment "
            "groups using an appropriate randomization procedure. Sample size, statistical "
            "power, minimum detectable effect, and experiment duration should be considered "
            "in advance. The outcomes should then be analyzed using an appropriate statistical "
            "method while checking experimental validity and relevant guardrail metrics."
        ),
        "key_concepts": [
            "A clear hypothesis and primary outcome metric should be defined before analyzing the experiment.",
            "Eligible experimental units should be assigned to control and treatment groups using an appropriate randomization procedure.",
            "Sample size, statistical power, minimum detectable effect, and experiment duration should be considered in advance.",
            "The treatment and control outcomes should be analyzed using an appropriate statistical method while checking experimental validity and relevant guardrail metrics."
        ],
        "acceptable_examples": [
            "Users can be randomly assigned to the existing product experience or the new feature.",
            "Conversion rate can be selected as a primary metric when it matches the business objective.",
            "Guardrail metrics can be monitored to detect undesirable side effects."
        ]
    },

    "DA_H04": {
        "question": (
            "How would you investigate a sudden decrease in monthly sales using data?"
        ),
        "reference_answer": (
            "A sudden decrease in monthly sales should first be verified by checking "
            "data quality, metric definitions, and reporting or pipeline changes. Sales "
            "can then be segmented by dimensions such as time, product, region, channel, "
            "or customer group to localize the decline. Historical trends, seasonality, "
            "promotions, pricing, inventory, customer behavior, and other relevant factors "
            "should be investigated, and possible explanations should be tested against "
            "evidence before conclusions are drawn."
        ),
        "key_concepts": [
            "The decline should first be verified by checking data quality, metric definitions, and reporting or pipeline changes.",
            "Sales should be segmented by relevant dimensions such as time, product, region, channel, or customer group to localize the decline.",
            "Historical trends, seasonality, promotions, pricing, inventory, customer behavior, and other relevant internal factors should be investigated.",
            "Potential explanations should be tested against evidence before drawing conclusions."
        ],
        "acceptable_examples": [
            "Compare sales by region to determine whether the decrease is concentrated geographically.",
            "Check whether stock shortages coincide with lower sales for particular products.",
            "Compare the same period with previous periods while considering seasonality."
        ]
    }
}


# ============================================================
# EXPECTED IDS
# ============================================================

EXPECTED_DATA_ANALYST_IDS = {
    "DA_E01",
    "DA_E02",
    "DA_E03",
    "DA_E04",

    "DA_M01",
    "DA_M02",
    "DA_M03",
    "DA_M04",

    "DA_H01",
    "DA_H02",
    "DA_H03",
    "DA_H04"
}


# ============================================================
# VALIDATOR
# ============================================================

def validate_data_analyst_references():

    actual_ids = set(
        DATA_ANALYST_REFERENCES.keys()
    )

    errors = []

    missing = (
        EXPECTED_DATA_ANALYST_IDS
        - actual_ids
    )

    extra = (
        actual_ids
        - EXPECTED_DATA_ANALYST_IDS
    )

    if missing:
        errors.append(
            "Missing IDs: "
            + ", ".join(sorted(missing))
        )

    if extra:
        errors.append(
            "Unexpected IDs: "
            + ", ".join(sorted(extra))
        )

    for question_id, reference in (
        DATA_ANALYST_REFERENCES.items()
    ):

        question = reference.get(
            "question"
        )

        reference_answer = reference.get(
            "reference_answer"
        )

        concepts = reference.get(
            "key_concepts"
        )

        examples = reference.get(
            "acceptable_examples"
        )

        if not question:
            errors.append(
                f"{question_id}: question is empty."
            )

        if (
            not isinstance(reference_answer, str)
            or not reference_answer.strip()
        ):
            errors.append(
                f"{question_id}: "
                "reference_answer is missing."
            )

        if (
            not isinstance(concepts, list)
            or len(concepts) == 0
        ):
            errors.append(
                f"{question_id}: "
                "key_concepts are missing."
            )

        if not isinstance(
            examples,
            list
        ):
            errors.append(
                f"{question_id}: "
                "acceptable_examples must be a list."
            )

    return {
        "valid": len(errors) == 0,
        "reference_count": len(actual_ids),
        "errors": errors
    }