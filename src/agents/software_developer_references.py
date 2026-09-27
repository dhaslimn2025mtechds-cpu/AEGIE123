# ============================================================
# AEGIE SOFTWARE DEVELOPER REFERENCE KNOWLEDGE
# ============================================================
#
# Purpose:
# Reference concepts for semantic evaluation of the
# 12 Software Developer interview questions.
#
# IMPORTANT:
# - These are NOT participant answers.
# - These are NOT primary dataset samples.
# - These are development-stage semantic reference resources.
# - reference_answer supports whole-answer and sentence-level comparison.
# - key_concepts support concept-level evidence.
# - They should be expert-reviewed before the final study.
# ============================================================


SOFTWARE_DEVELOPER_REFERENCES = {

    # ========================================================
    # EASY
    # ========================================================

    "SD_E01": {
        "question": (
            "What is the difference between a list "
            "and a tuple in Python?"
        ),
        "reference_answer": (
            "In Python, a list and a tuple can both store multiple ordered values. "
            "A list is mutable, so its elements can be changed after creation, "
            "while a tuple is immutable and its elements cannot normally be changed "
            "after creation. Lists use square brackets, while tuples commonly use "
            "parentheses."
        ),
        "key_concepts": [
            "A list is mutable, so its elements can be changed after creation.",
            "A tuple is immutable, so its elements cannot normally be changed after creation.",
            "Lists use square brackets while tuples commonly use parentheses.",
            "Both can store multiple ordered values."
        ],
        "acceptable_examples": [
            "A list can be written as [1, 2, 3].",
            "A tuple can be written as (1, 2, 3)."
        ]
    },

    "SD_E02": {
        "question": (
            "What is object-oriented programming?"
        ),
        "reference_answer": (
            "Object-oriented programming organizes software using classes and objects. "
            "A class defines the attributes and behavior that its objects can have, "
            "and an object is an instance of a class. Common object-oriented concepts "
            "include encapsulation, inheritance, polymorphism, and abstraction."
        ),
        "key_concepts": [
            "Object-oriented programming organizes software around objects and classes.",
            "A class defines attributes and behavior that objects can have.",
            "Objects are instances of classes.",
            "Common object-oriented concepts include encapsulation, inheritance, polymorphism, and abstraction."
        ],
        "acceptable_examples": [
            "A Car class can define attributes such as speed and methods such as start.",
            "Different objects can be created from the same class."
        ]
    },

    "SD_E03": {
        "question": (
            "What is the difference between a compiler "
            "and an interpreter?"
        ),
        "reference_answer": (
            "A compiler translates source code into another form before program "
            "execution, while an interpreter processes or executes instructions "
            "during runtime. Compilation can produce an executable or an intermediate "
            "representation. These approaches can also be combined, so a language "
            "implementation does not always use only one of them."
        ),
        "key_concepts": [
            "A compiler translates source code into another form before program execution.",
            "An interpreter executes or processes program instructions during runtime.",
            "Compiled programs can produce a separate executable or intermediate representation.",
            "Compilation and interpretation are implementation strategies and some languages use a combination of both."
        ],
        "acceptable_examples": [
            "C implementations commonly compile source code before execution.",
            "Python implementations can compile source into bytecode that is then executed by a virtual machine."
        ]
    },

    "SD_E04": {
        "question": (
            "What is an API?"
        ),
        "reference_answer": (
            "An API, or application programming interface, defines how software "
            "components communicate or interact with each other. It can expose "
            "operations, functions, endpoints, or data contracts. This allows one "
            "system to use another system's functionality without needing to know "
            "all of its internal implementation details."
        ),
        "key_concepts": [
            "An API is an application programming interface.",
            "An API defines how software components can communicate or interact.",
            "It exposes defined operations, functions, endpoints, or data contracts.",
            "APIs allow systems to use functionality without needing to know all internal implementation details."
        ],
        "acceptable_examples": [
            "A web application can call a weather API to obtain weather data.",
            "A REST API may expose endpoints for creating or retrieving resources."
        ]
    },


    # ========================================================
    # MEDIUM
    # ========================================================

    "SD_M01": {
        "question": (
            "Explain the difference between a process "
            "and a thread."
        ),
        "reference_answer": (
            "A process is an executing program with its own address space and process "
            "resources, while a thread is an execution unit that runs within a process. "
            "Threads in the same process normally share memory and resources. Processes "
            "generally provide stronger isolation, whereas threads can communicate "
            "through shared memory more directly."
        ),
        "key_concepts": [
            "A process is an executing program with its own process resources and address space.",
            "A thread is an execution unit within a process.",
            "Threads in the same process normally share process memory and resources.",
            "Processes generally have stronger isolation while threads can communicate through shared memory more directly."
        ],
        "acceptable_examples": [
            "A browser can use multiple processes while each process may contain multiple threads.",
            "Threads can perform concurrent tasks within one application process."
        ]
    },

    "SD_M02": {
        "question": (
            "How would you handle exceptions "
            "in a software application?"
        ),
        "reference_answer": (
            "Exceptions should be handled at a level where the application can respond "
            "to them meaningfully. Specific exception types should generally be handled "
            "rather than hiding every error, and useful diagnostic information should "
            "be logged. When possible, the application should recover safely or fail "
            "gracefully without corrupting data or exposing sensitive information."
        ),
        "key_concepts": [
            "Exceptions should be caught at an appropriate level where the program can meaningfully handle them.",
            "Specific exception types should generally be handled instead of hiding every possible error.",
            "Errors should be logged with useful diagnostic information.",
            "The application should recover safely when possible or fail gracefully without corrupting data or exposing sensitive information."
        ],
        "acceptable_examples": [
            "A failed database operation can be caught, logged, and rolled back.",
            "A user can receive a clear error message while technical details are recorded in application logs."
        ]
    },

    "SD_M03": {
        "question": (
            "Explain REST API and common HTTP methods."
        ),
        "reference_answer": (
            "REST is an architectural style commonly used to build resource-oriented "
            "web APIs, where resources are identified through URIs or endpoints. GET "
            "is commonly used to retrieve a resource, POST for creation, PUT or PATCH "
            "for modification, and DELETE for deletion. These HTTP methods allow clients "
            "to perform common operations on resources through defined endpoints."
        ),
        "key_concepts": [
            "REST is an architectural style commonly used for resource-oriented web APIs.",
            "Resources are identified through URIs or endpoints.",
            "GET is commonly used to retrieve a resource.",
            "POST, PUT or PATCH, and DELETE are commonly used for creation, modification, and deletion operations respectively."
        ],
        "acceptable_examples": [
            "GET /users can retrieve users.",
            "POST /users can create a new user.",
            "DELETE /users/10 can request deletion of a user resource."
        ]
    },

    "SD_M04": {
        "question": (
            "What is database indexing "
            "and why is it useful?"
        ),
        "reference_answer": (
            "A database index is an auxiliary data structure that helps locate rows "
            "more efficiently. A suitable index can reduce the amount of data scanned "
            "and improve retrieval, filtering, joining, or ordering performance. "
            "Indexes also have costs, including additional storage and maintenance "
            "during inserts, updates, or other data modifications."
        ),
        "key_concepts": [
            "A database index is an auxiliary data structure used to locate rows more efficiently.",
            "Indexes can reduce the amount of data that must be scanned for suitable queries.",
            "Indexes can improve retrieval, filtering, joining, or ordering performance depending on the query and index design.",
            "Indexes have costs such as additional storage and maintenance during data modifications."
        ],
        "acceptable_examples": [
            "An index on a frequently searched customer ID can speed up matching queries.",
            "Adding unnecessary indexes can increase the cost of inserts and updates."
        ]
    },


    # ========================================================
    # HARD
    # ========================================================

    "SD_H01": {
        "question": (
            "How would you design a scalable application "
            "that handles many concurrent users?"
        ),
        "reference_answer": (
            "A scalable application can distribute traffic across multiple application "
            "instances using load balancing and can scale resources according to workload "
            "requirements. Shared components such as databases, caches, and external "
            "services must also be designed to avoid bottlenecks. Depending on the system, "
            "techniques such as stateless services, caching, asynchronous processing, "
            "monitoring, and capacity planning can support larger concurrent workloads."
        ),
        "key_concepts": [
            "The system should support horizontal or vertical scaling based on workload requirements.",
            "Traffic can be distributed across application instances using load balancing.",
            "Shared bottlenecks such as databases, caches, and external services must also be designed for scale.",
            "The design should include monitoring, capacity planning, and techniques such as caching, asynchronous processing, or stateless services where appropriate."
        ],
        "acceptable_examples": [
            "Multiple stateless application instances can run behind a load balancer.",
            "Frequently requested data can be cached to reduce database load.",
            "Background queues can process long-running work asynchronously."
        ]
    },

    "SD_H02": {
        "question": (
            "How would you identify and improve "
            "a performance bottleneck in an application?"
        ),
        "reference_answer": (
            "A performance bottleneck should first be measured and localized using tools "
            "such as profiling, monitoring, tracing, logs, or appropriate benchmarks. "
            "Possible bottlenecks include CPU, memory, disk, network, database queries, "
            "locking, and external dependencies. After making an optimization, the same "
            "workload and relevant metrics should be measured again to verify improvement "
            "and check for regressions."
        ),
        "key_concepts": [
            "Performance should first be measured using profiling, monitoring, tracing, logs, or appropriate benchmarks.",
            "The bottleneck should be localized before making optimizations.",
            "Potential bottlenecks can involve CPU, memory, disk, network, database queries, locking, or external dependencies.",
            "After optimization the same workload and relevant metrics should be measured again to verify improvement and detect regressions."
        ],
        "acceptable_examples": [
            "A profiler can identify a function consuming excessive CPU time.",
            "A slow database query can be investigated using query execution information and improved with an appropriate query or index.",
            "Load testing can compare performance before and after a change."
        ]
    },

    "SD_H03": {
        "question": (
            "Explain how you would prevent race conditions "
            "in a concurrent application."
        ),
        "reference_answer": (
            "A race condition occurs when the correctness of concurrent operations depends "
            "on their timing or interleaving while accessing shared state. Shared mutable "
            "state should therefore be minimized or synchronized using an appropriate "
            "mechanism such as locks, mutexes, semaphores, atomic operations, transactions, "
            "or message passing. The synchronization design should also consider deadlocks, "
            "contention, and performance."
        ),
        "key_concepts": [
            "A race condition occurs when correctness depends on the timing or interleaving of concurrent operations on shared state.",
            "Shared mutable state should be minimized or properly synchronized.",
            "Synchronization mechanisms can include locks, mutexes, semaphores, atomic operations, transactions, or message passing depending on the system.",
            "Synchronization design should also consider problems such as deadlocks, contention, and performance."
        ],
        "acceptable_examples": [
            "A lock can protect a critical section that modifies shared data.",
            "An atomic operation can safely update a shared counter when supported.",
            "Database transactions can protect related database changes."
        ]
    },

    "SD_H04": {
        "question": (
            "How would you design a fault-tolerant service "
            "when one dependency may become unavailable?"
        ),
        "reference_answer": (
            "A fault-tolerant service should detect and handle dependency failures without "
            "allowing them to cause uncontrolled cascading failures. Timeouts can limit "
            "waiting, and carefully controlled retries with backoff can help with suitable "
            "transient failures. Depending on the dependency, circuit breakers, fallback "
            "behavior, redundancy, queues, or graceful degradation can improve resilience."
        ),
        "key_concepts": [
            "The service should detect and handle dependency failures without uncontrolled cascading failure.",
            "Timeouts should limit how long the service waits for an unavailable dependency.",
            "Retries can be used for suitable transient failures with limits and backoff.",
            "Techniques such as circuit breakers, fallback behavior, redundancy, queues, or graceful degradation can improve resilience depending on the dependency."
        ],
        "acceptable_examples": [
            "A circuit breaker can temporarily stop repeated calls to a failing dependency.",
            "Exponential backoff can reduce repeated retry pressure.",
            "A service may return cached information or reduced functionality when a noncritical dependency is unavailable."
        ]
    }
}


# ============================================================
# VALIDATION
# ============================================================

EXPECTED_SOFTWARE_DEVELOPER_IDS = {
    "SD_E01",
    "SD_E02",
    "SD_E03",
    "SD_E04",

    "SD_M01",
    "SD_M02",
    "SD_M03",
    "SD_M04",

    "SD_H01",
    "SD_H02",
    "SD_H03",
    "SD_H04"
}


def validate_software_developer_references():

    actual_ids = set(
        SOFTWARE_DEVELOPER_REFERENCES.keys()
    )

    missing = (
        EXPECTED_SOFTWARE_DEVELOPER_IDS
        - actual_ids
    )

    extra = (
        actual_ids
        - EXPECTED_SOFTWARE_DEVELOPER_IDS
    )

    errors = []

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
        SOFTWARE_DEVELOPER_REFERENCES.items()
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