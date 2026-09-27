# ============================================================
# AEGIE DATA SCIENTIST REFERENCE KNOWLEDGE
# ============================================================
#
# Purpose:
# Provides development-stage reference knowledge for the
# 12 Data Scientist interview questions.
#
# IMPORTANT:
# - These are NOT participant responses.
# - These are NOT human annotation labels.
# - These are NOT primary dataset samples.
# - reference_answer is development reference knowledge used
#   for semantic comparison.
# - key_concepts remain the concept-level evidence source.
# - All reference content should be expert-reviewed before any
#   final research experiment or validated scoring claim.
# ============================================================


REFERENCE_ANSWERS = {

    # ========================================================
    # EASY
    # ========================================================

    "DS_E01": {

        "question":
            "What is the difference between supervised "
            "and unsupervised learning?",

        "reference_answer": (
            "Supervised learning learns from labeled data, where "
            "training examples contain input-output pairs. It is "
            "commonly used for tasks such as classification and "
            "regression. Unsupervised learning works with unlabeled "
            "data and attempts to discover patterns or structure in "
            "the data, such as groups identified through clustering."
        ),

        "key_concepts": [
            "Supervised learning uses labeled data.",
            "Supervised learning learns from input-output pairs.",
            "Unsupervised learning uses unlabeled data.",
            "Unsupervised learning discovers patterns or structure."
        ],

        "acceptable_examples": [
            "Classification",
            "Regression",
            "Clustering"
        ]
    },


    "DS_E02": {

        "question":
            "What is overfitting in machine learning?",

        "reference_answer": (
            "Overfitting occurs when a model learns the training "
            "data too closely, including noise or irrelevant "
            "patterns. The model may show very strong performance "
            "on the training data but perform poorly on unseen "
            "data. This indicates weak generalization beyond the "
            "examples used during training."
        ),

        "key_concepts": [
            "The model learns the training data too closely.",
            "The model may also learn noise or irrelevant patterns.",
            "Training performance can be high.",
            "Performance on unseen data is poor."
        ],

        "acceptable_examples": [
            "High training accuracy but low test accuracy."
        ]
    },


    "DS_E03": {

        "question":
            "What is the difference between a population "
            "and a sample?",

        "reference_answer": (
            "A population is the complete group of individuals, "
            "items, or observations that a study is interested in. "
            "A sample is a subset selected from that population. "
            "Samples are commonly analyzed to make inferences about "
            "the larger population."
        ),

        "key_concepts": [
            "Population is the complete group of interest.",
            "A sample is a subset of the population.",
            "Samples are used to make inferences about a population."
        ],

        "acceptable_examples": [
            "All customers versus a selected group of customers."
        ]
    },


    "DS_E04": {

        "question":
            "Why do we split a dataset into training "
            "and testing data?",

        "reference_answer": (
            "A dataset is split so that one portion can be used to "
            "train or fit the model while a separate testing portion "
            "is kept away from training. The test data is then used "
            "to estimate how the trained model performs on unseen "
            "examples. This helps evaluate the model's ability to "
            "generalize."
        ),

        "key_concepts": [
            "Training data is used to fit the model.",
            "Testing data is kept separate from training.",
            "Testing estimates performance on unseen data.",
            "The split helps evaluate generalization."
        ],

        "acceptable_examples": [
            "Train the model on one portion and evaluate "
            "it on a separate portion."
        ]
    },


    # ========================================================
    # MEDIUM
    # ========================================================

    "DS_M01": {

        "question":
            "Explain the bias-variance tradeoff in "
            "machine learning.",

        "reference_answer": (
            "The bias-variance tradeoff describes the balance "
            "between errors caused by a model being too simple and "
            "errors caused by a model being too sensitive to the "
            "training data. High bias is associated with "
            "underfitting, while high variance is associated with "
            "overfitting. Reducing one can sometimes increase the "
            "other, so the objective is to find a model that "
            "generalizes well to unseen data."
        ),

        "key_concepts": [
            "High bias is associated with underfitting.",
            "High variance is associated with overfitting.",
            "Reducing one can increase the other.",
            "The objective is good generalization to unseen data."
        ],

        "acceptable_examples": [
            "A very simple model may underfit while a very "
            "complex model may overfit."
        ]
    },


    "DS_M02": {

        "question":
            "What is cross-validation and why is it useful?",

        "reference_answer": (
            "Cross-validation is an evaluation procedure in which "
            "data is divided into multiple folds. The model is "
            "trained and validated multiple times, with different "
            "folds used for validation across the runs. This provides "
            "a more robust estimate of model performance than relying "
            "on a single validation split."
        ),

        "key_concepts": [
            "Data is divided into multiple folds.",
            "The model is trained and validated multiple times.",
            "Different folds are used for validation.",
            "It provides a more robust estimate of model performance."
        ],

        "acceptable_examples": [
            "K-fold cross-validation."
        ]
    },


    "DS_M03": {

        "question":
            "What is the difference between L1 and "
            "L2 regularization?",

        "reference_answer": (
            "L1 regularization penalizes the absolute magnitude of "
            "model coefficients, while L2 regularization penalizes "
            "their squared values. L1 can drive some coefficients "
            "exactly to zero and can therefore produce sparse models. "
            "L2 generally shrinks coefficient values without forcing "
            "many of them exactly to zero."
        ),

        "key_concepts": [
            "L1 regularization uses the absolute magnitude "
            "of coefficients.",
            "L2 regularization uses squared coefficient values.",
            "L1 can drive some coefficients to zero.",
            "L2 generally shrinks coefficients without forcing "
            "many exactly to zero."
        ],

        "acceptable_examples": [
            "Lasso uses L1 regularization.",
            "Ridge uses L2 regularization."
        ]
    },


    "DS_M04": {

        "question":
            "How would you handle an imbalanced "
            "classification dataset?",

        "reference_answer": (
            "For an imbalanced classification dataset, accuracy "
            "alone can be misleading because the majority class can "
            "dominate the result. Evaluation should use metrics that "
            "match the problem and error costs, such as precision, "
            "recall, F1 score, or PR-AUC where appropriate. "
            "Resampling methods or class weighting can also be "
            "considered depending on the data and objective."
        ),

        "key_concepts": [
            "Accuracy alone can be misleading.",
            "Use suitable evaluation metrics.",
            "Resampling or class weighting can be considered.",
            "The choice depends on the problem and error costs."
        ],

        "acceptable_examples": [
            "Precision",
            "Recall",
            "F1 score",
            "PR-AUC",
            "Class weights",
            "Oversampling",
            "Undersampling"
        ]
    },


    # ========================================================
    # HARD
    # ========================================================

    "DS_H01": {

        "question":
            "How would you detect and prevent data leakage "
            "in a machine learning project?",

        "reference_answer": (
            "Data leakage occurs when information that would not be "
            "available at prediction time influences model training "
            "or evaluation. To prevent it, training and test data "
            "should be separated correctly, and preprocessing steps "
            "such as scaling or imputation should be fitted using "
            "training data only. Feature construction should also "
            "respect time and prediction boundaries when relevant. "
            "Features containing future or otherwise unavailable "
            "information should be identified and removed."
        ),

        "key_concepts": [
            "Information unavailable at prediction time must not "
            "leak into model training.",
            "Train and test data must be separated correctly.",
            "Preprocessing should be fitted using training data.",
            "Feature construction should respect time or prediction "
            "boundaries when relevant."
        ],

        "acceptable_examples": [
            "Fit a scaler only on the training data.",
            "Use time-based splitting for temporal prediction.",
            "Remove features containing future information."
        ]
    },


    "DS_H02": {

        "question":
            "How would you select an appropriate evaluation "
            "metric for an imbalanced classification problem?",

        "reference_answer": (
            "The evaluation metric should be selected according to "
            "the application objective and the consequences of false "
            "positives and false negatives. Accuracy can be "
            "misleading when classes are highly imbalanced. Recall "
            "is useful when missing positive cases is especially "
            "costly, while precision is important when false "
            "positive predictions are costly. F1 or PR-AUC can be "
            "useful when the problem requires a broader view of "
            "positive-class performance."
        ),

        "key_concepts": [
            "Metric selection depends on the application objective.",
            "False-positive and false-negative costs should "
            "be considered.",
            "Accuracy may be misleading with class imbalance.",
            "Precision and recall measure different error tradeoffs."
        ],

        "acceptable_examples": [
            "Recall when missing positive cases is costly.",
            "Precision when false alarms are costly.",
            "F1 when balancing precision and recall is useful.",
            "PR-AUC for imbalanced positive-class evaluation."
        ]
    },


    "DS_H03": {

        "question":
            "How would you determine whether adding a new "
            "feature genuinely improves a predictive model?",

        "reference_answer": (
            "To determine whether a new feature genuinely improves "
            "a model, compare otherwise comparable models trained "
            "with and without that feature. Both models should use "
            "the same evaluation protocol and an appropriate metric "
            "on validation or other unseen data. The improvement "
            "should also be checked across repeated evaluations or "
            "cross-validation folds to determine whether it is "
            "stable rather than an artifact of one split."
        ),

        "key_concepts": [
            "Compare models with and without the new feature.",
            "Use the same evaluation protocol for both models.",
            "Evaluate using unseen or validation data.",
            "Use an appropriate performance metric.",
            "Check whether the improvement is stable across "
            "repeated evaluations or folds."
        ],

        "acceptable_examples": [
            "Cross-validation",
            "Ablation comparison",
            "Confidence intervals",
            "Statistical comparison where appropriate"
        ]
    },


    "DS_H04": {

        "question":
            "How would you investigate a machine learning "
            "model that performs well during training but "
            "poorly on new data?",

        "reference_answer": (
            "Strong training performance combined with poor "
            "performance on new data can indicate overfitting, but "
            "other causes should also be investigated. I would check "
            "for train-test distribution differences, data leakage, "
            "incorrect evaluation, and problems in preprocessing or "
            "feature pipelines. I would also review model complexity "
            "and regularization and use validation methods such as "
            "cross-validation or learning curves to better understand "
            "the generalization problem."
        ),

        "key_concepts": [
            "Investigate possible overfitting.",
            "Check for train-test distribution differences.",
            "Check for data leakage or incorrect evaluation.",
            "Review model complexity and regularization.",
            "Validate preprocessing and feature pipelines."
        ],

        "acceptable_examples": [
            "Cross-validation",
            "Learning curves",
            "Regularization",
            "Simpler model",
            "More representative training data"
        ]
    }
}


# ============================================================
# GET REFERENCE ANSWER
# ============================================================

def get_reference_answer(question_id):

    return REFERENCE_ANSWERS.get(
        question_id
    )


# ============================================================
# VALIDATE KNOWLEDGE BASE
# ============================================================

def validate_reference_answers():

    expected_ids = {

        "DS_E01",
        "DS_E02",
        "DS_E03",
        "DS_E04",

        "DS_M01",
        "DS_M02",
        "DS_M03",
        "DS_M04",

        "DS_H01",
        "DS_H02",
        "DS_H03",
        "DS_H04"
    }

    actual_ids = set(
        REFERENCE_ANSWERS.keys()
    )

    if actual_ids != expected_ids:

        missing = (
            expected_ids - actual_ids
        )

        extra = (
            actual_ids - expected_ids
        )

        return (
            False,
            f"Missing={missing}, Extra={extra}"
        )

    for question_id, data in (
        REFERENCE_ANSWERS.items()
    ):

        if not data.get("question"):

            return (
                False,
                f"{question_id}: question missing."
            )

        reference_answer = data.get(
            "reference_answer"
        )

        if (
            not isinstance(
                reference_answer,
                str
            )
            or not reference_answer.strip()
        ):

            return (
                False,
                f"{question_id}: reference_answer missing."
            )

        if not data.get("key_concepts"):

            return (
                False,
                f"{question_id}: key concepts missing."
            )

        if not isinstance(
            data["key_concepts"],
            list
        ):

            return (
                False,
                f"{question_id}: key_concepts must be a list."
            )

        if not isinstance(
            data.get(
                "acceptable_examples",
                []
            ),
            list
        ):

            return (
                False,
                f"{question_id}: acceptable_examples "
                f"must be a list."
            )

    return (
        True,
        "All 12 Data Scientist references are valid."
    )