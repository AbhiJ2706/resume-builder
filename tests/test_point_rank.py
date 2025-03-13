import textwrap

import pytest

from resume_builder.job_posting import JobPosting
from resume_builder.data_builder import top_k_points


def swe_posting():
    return textwrap.dedent(
        """
        What You Get To Do

            Craft microservices, components, & tools to automate the life cycle of highly available (HA), distributed services and applications on multiple platforms!
            Engineer quality, scalability, availability, and security into your code
            Protect your products with the assurances of automated testing
            Deploy containerized applications to AWS through your Continuous Integration (CI) and Continuous Deployment
            Work with highly skilled team members, operations team, product managers, and architects as we collaborate to write code / algorithms, mentor one another and build infrastructure and software that matters

        What you bring to Guidewire:

            Software development skills in one or more of the following frameworks & languages: Java / Golang / NodeJS / Python / equivalent
            Container technologies: Docker, Linux debugging
            Strong interpersonal skills, a demeanor emphasizing team wins over individual success
            Comfort working in an agile, social and fast-paced environment

        Nice to Have

            Advocate of cloud platforms (like Kubernetes / Mesos / Cloud Foundry / OpenShift, AWS / GCP / Azure, Serverless)
            Experience with Spring Boot / Bash programming skills
            BS/MS degree (Computer Science or Math) or equivalent level of proven professional proficiency
        """
    )


def ml_posting():
    return textwrap.dedent(
        """
        What you will do:

            Contribute to advancing NLP and its applications, to create highly innovative products and customer experiences, ranging from text understanding and classification to information extraction.
            Build end-to-end products from the ground up, from data exploration through feature generation, model construction and deployment.
            Review and choose the best and most appropriate annotated datasets for the best-supervised learning methods.
            Independently identify AI/ML opportunities, define key product metrics and propose solutions to leadership.
            Stay up to date with emerging technologies in GenAI/LLM field and recommend improvements to existing AI models and products.

        Basic Qualifications

            3+ years of proven experience delivering applied deep learning products in NLP (e.g., Named Entity Recognition, Question Answering), including taking a product through design, implementation, and to production
            3+ years of developing Machine Learning driven features in Python with proficiency in deep learning frameworks (e.g., Tensorflow, Pytorch)
            3+ years in fields of NLP via delivering enterprise-grade code with deep learning architectures (e.g., RNNs, CNNs, Transformers)
            1+ years of experience researching (e.g., fine-tuning), prototyping, and productionalizing LLM-based solutions using frameworks such as Huggingface, Langchain, and LlamaIndex.

        Other Qualifications

            Experience with Git or other distributed version control systems 
            Experience building Extract Transform Load (ETL) pipelines
            Experience in designing and crafting experiments, A/B testing and data analysis in the domain of quality metrics for machine learning services.
            Outstanding communication skills with ability to communicate results clearly to non-technical audiences with a focus on driving impact
            Experience using distributed processing architecture and ML/ Data platform (e.g., AWS Sagemaker, Databricks, Spark, Kubeflow, etc); building experience is a plus
            Experience with Computer Vision is a plus
            Bachelor's degree or equivalent in Computer Science, Mathematics, Statistics
        """
    )


def embedded_posting():
    return textwrap.dedent(
        """
        The Embedded Software Engineer is responsible for creating embedded software which controls and monitors 
        medical gas distribution in medical facilities. Working with a group, the embedded software engineer will create well 
        documented software which will run on an embedded hardware platform. Software needs vary from board-level hardware specific 
        drivers to GUI development. In addition to new product development, the Software Engineer is responsible for maintaining 
        existing software projects, keeping them up-to-date and functional on modern architecture as well as supporting customers by 
        troubleshooting software issues with installed products.

        What we expect of you? 

            Experience with an Integrated Development Environment to program microcontrollers using the C and C++ programming language is a must. 
            Applicant should have experience using tools like Azure DevOps or Atlassian Suite of products to complete necessary tasks and provide information needed for tracking the project. Applicant should have experience working with Microsoft Office Applications including Word, Excel, and Access. Electronics experience including understanding schematics, and working with DC power supplies, soldering stations, and multi-meters is a bonus.
            Minimum 4 Years BS Degree in Electrical Engineering, Computer Engineering, or Computer Science.
            Experience working with embedded systems or low-level hardware development.
            Comfortable debugging software running on a hardware platform connected by a JTAG interface.
            Must have excellent organizational, interpersonal, verbal and written communication, and software engineering skills.
            Must be able to work both independently and as a productive member of a team.
        """
    )


def cloud_posting():
    return textwrap.dedent(
        """
        As a Software Developer on our Cloud team, you'll tackle diverse challenges and focus on crafting innovative solutions. Your curiosity, problem-solving skills, and coding expertise will bring fresh ideas to life. By contributing to Verafin, you'll help combat crimes like human trafficking, elder abuse, and drug trafficking, joining a passionate team dedicated to making a difference. At Verafin, being a Developer means positively impacting the world while doing what you love - solving complex problems with the power of code. We are hiring across several of our cloud teams, looking for various levels of experience.

        Role Responsibilities

            Solid understanding of AWS and cloud solutions architecture 
            Keep up to date with new AWS and cloud solutions 
            Build, automate and secure application configuration, auto deployment and provisioning services 
            Design, develop, automate and operationalize software/service updates 
            Develop innovative ways to measure and monitor application and infrastructure health 
            Work with engineering and product management to build and manage features that are highly available, high performance, and secure 
            Automate deployment, customization, upgrades, and monitoring through modern DevOps tools including Terraform and AWS Cloud formation 

        Essential Skills & Qualifications

            A university degree or college diploma in Computer Engineering, Computer Science, or equivalent experience 
            Experience with microservices and data lakes 
            Able to design and build systems using Amazon Web Services 
            Knowledge of distributed systems 
            Experience with Linux systems, virtualization, and network administration 
            Proficiency in Java, Python and Bash 
            Understanding of security principles 
            AWS certifications would be an asset 

        What does success look like in this role?

            Understanding the goals of the team while using problem solving skills 
            Developing cloud-based services that have good uptime, health, and security 
            Producing clean and efficient code 
            Consistently iterating on coding practices for continuous improvement 

        What does growth look like in this role?

            Develop along the technical leadership path including Lead Developer and Architect 

        This position can be located in St. John's or Toronto, and offers the opportunity for a hybrid work environment (2 days a week in office), providing flexibility and accessibility for qualified candidates.
        """
    )


def startup_posting():
    return textwrap.dedent(
        """
        Join the team at Wisedocs AI as a Sr. Back-End Software Developer, where you will be instrumental in building the architecture that powers our leading-edge medical data processing system. Our application interfaces seamlessly with our advanced AI/ML platform, leveraging computer vision and generative models to make sense of intricate legal and medical documents for efficient medical claim processing.

        The position is a hybrid model requiring on-site presence at least twice/week in Downtown Toronto.

        As a key member of the Engineering team, your responsibilities will include:

            Designing, building, and maintaining efficient, reusable, and reliable Python code that powers our back-end systems and ML pipeline
            Identifying and resolving performance and scalability issues, helping to improve the robustness of our system
            Handling complex data structures and algorithms, ensuring the seamless processing of data in our system
            Taking on additional responsibilities as needed, demonstrating flexibility and adaptability in a dynamic working environment
            Creating comprehensive technical documentation for system components and architecture, thereby providing clarity on architectural decisions and engineering contributions across the team
            Working in collaboration with front-end developers to integrate user-facing elements with server-side logic, creating a seamless user experience
            other duties as assigned

        Qualifications

            A minimum of 5 years of experience as a Back-End Developer with extensive experience in Python, showcasing a deep understanding of the language
            Proficiency in using Python frameworks such as Django or Flask
            Experience with database systems like SQL or NoSQL
            Strong familiarity with cloud platforms like AWS, Google Cloud, or Azure
            An understanding of automation practices throughout the Agile development, build, and deployment phases of the application lifecycle
            A robust problem-solving mindset; comfortable navigating frequently changing work items and scopes, and capable of managing multiple tasks efficiently
        """
    )


def big_company_posting():
    return textwrap.dedent(
        """
        AWS service teams spend a significant amount of their development effort on creating, maintaining and improving their Control Plane software. This means the cost of offering a new piece of software as a managed service is often orders of magnitude higher than simply creating the new software. The AWS Alameda centralizes this work, saving each of these many AWS teams the cost of creating, maintaining and improving Control Planes. Alameda automates the creation and maintenance of infrastructure and software for both the Control Plane and the Data Plane of newly managed services. Alameda offers building blocks that fully abstract a single functionality as a managed services, which can be extended to offer custom business logic for a specific AWS Service. Alameda offers the full control plane for AWS Services by allowing seamless composition of building blocks that work together to provide a full managed AWS service experience.

        We are looking for world-class software developers who like to deliver software solutions that solve business problems and delight your customers with efficiency and productivity gains. You have development experience with technologies like AWS, Java, TypeScript, CDK, and DynamoDB.

        Basic Qualifications

            3+ years of non-internship professional software development experience
            2+ years of non-internship design or architecture (design patterns, reliability and scaling) of new and existing systems experience
            Experience programming with at least one software programming language

        Preferred Qualifications

            3+ years of full software development life cycle, including coding standards, code reviews, source control management, build processes, testing, and operations experience
            Bachelor's degree in computer science or equivalent
        """
    )


@pytest.fixture
def very_different_points():
    return [
        {
            "summary": "Streamlined and secured data processing pipelines. Automated essential ETL tasks, saving engineers 1000+ hours.",
            "required_skills": ["Terraform"]
        },
        {
            "summary": "Created an app to send advertiser leads to sales managers through Slack, improving lead retrieval for 1000+ people.",
            "required_skills": ["Kotlin", "Typescript", "AWS"]
        },
        {
            "summary": "Implemented, tested, and deployed an ML model to recommend code reviewers for pull requests, serving 3600+ users.",
            "required_skills": ["Python", "Scikit-learn", "NumPy", "Pandas"]
        },
        {
            "summary": "Wrote automated unit tests for 5+ SRv6 features, ensuring correctness and scalability across network topologies.",
            "required_skills": ["Python"]
        },
        {
            "summary": "Refactored frontend and backend components, decreasing time to develop and deploy form-based services by 30%.",
            "required_skills": ["Kotlin", "Typescript"]
        },
        {
            "summary": "Added runtime configuration for embedded debugging infrastructure, increasing debugging speed for 40+ engineers.",
            "required_skills": ["C++"]
        },
    ]


@pytest.fixture
def very_similar_points():
    return [
        {
            "summary": "Created and deployed an Extract-Load-Transform (ELT) pipeline to analyze processor performance on AI workloads.",
            "required_skills": ["Python"]
        },
        {
            "summary": "Used a data-driven approach to speed up Inter-Process Communication (IPC) for an embedded AI accelerator by 50%.",
            "required_skills": ["C++", "Python"]
        },
        {
            "summary": "Implemented infrastructure to collect performance metrics for 5+ embedded AI-based image processing use cases.",
            "required_skills": ["C++"]
        },
        {
            "summary": "Designed and implemented a time-based search engine to enable nanosecond-level analysis of CNN execution.",
            "required_skills": ["Python", "NumPy", "Pandas"]
        }
    ]


@pytest.fixture
def ml_and_swe_points():
    return [
        {
            "summary": "Led the development of a deep learning-based transcript analysis pipeline, delivering 20+ user progress insights to BetterUp's partners.",
            "required_skills": ["Python"]
        },
        {
            "summary": "Extracted conversation insights from coaching session transcripts, enabling platform-wide quality analysis for 1M+ sessions.",
            "required_skills": ["Python"]
        },
        {
            "summary": "Developed a robust job title segmentation model, improving granularity of session transcript analysis.",
            "required_skills": ["Python"]
        },
        {
            "summary": "Designed an LLM-based assistant to convert language to database queries, accelerating data search times by 10x.",
            "required_skills": ["Kotlin", "Typescript", "AWS"]
        },
        {
            "summary": "Implemented, tested, and deployed an ML model to recommend code reviewers for pull requests, serving 3600+ users.",
            "required_skills": ["Python", "Scikit-learn", "NumPy", "Pandas"]
        },
        {
            "summary": "Developed a Recurrent Neural Network (RNN)-based model to detect anomalies in router telemetry data.",
            "required_skills": ["Python", "TensorFlow"]
        },
    ] + [
        {
            "summary": "Created an app to send advertiser leads to sales managers through Slack, improving lead retrieval for 1000+ people.",
            "required_skills": ["Kotlin", "Typescript", "AWS"]
        },
        {
            "summary": "Refactored frontend and backend components, decreasing time to develop and deploy form-based services by 30%.",
            "required_skills": ["Kotlin", "Typescript"]
        },
        {
            "summary": "Optimized Inter-Process Communication (IPC) for an embedded framework that accelerates image processing.",
            "required_skills": ["C++", "Android"]
        },
        {
            "summary": "Added runtime configuration for embedded debugging infrastructure, increasing debugging speed for 40+ engineers.",
            "required_skills": ["C++"]
        },
        {
            "summary": "Integrated data transmission features into production code, wrote tests to verify thread-safety and scalability.",
            "required_skills": ["C++", "Android"]
        },
    ]


@pytest.fixture
def leadership_independence_points():
    return [
        {
            "summary": "Led the development of a deep learning-based transcript analysis pipeline, delivering 20+ user progress insights to BetterUp's partners.",
            "required_skills": ["Python"]
        },
        {
            "summary": "Led development of a software profiling pipeline for analyzing the performance of CNNs running on Snapdragon.",
            "required_skills": ["Python", "Bash"]
        },
        {
            "summary": "Created and deployed an Extract-Load-Transform (ELT) pipeline to analyze processor performance on AI workloads.",
            "required_skills": ["Python"]
        },
        {
            "summary": "Designed and implemented a time-based search engine to enable nanosecond-level analysis of CNN execution.",
            "required_skills": ["Python", "NumPy", "Pandas"]
        }
    ] + [
        {
            "summary": "Refactored frontend and backend components, decreasing time to develop and deploy form-based services by 30%.",
            "required_skills": ["Kotlin", "Typescript"]
        },
        {
            "summary": "Increased speed of analysis tools by 500+%. Added reduction methods to accelerate preprocessing of large datasets.",
            "required_skills": ["Python"]
        },
        {
            "summary": "Optimized Inter-Process Communication (IPC) for an embedded framework that accelerates image processing.",
            "required_skills": ["C++", "Android"]
        },
        {
            "summary": "Optimized Natural Language Processing (NLP) pipelines for customer service chatbots, increasing accuracy to 99%.",
            "required_skills": ["Docker"]
        },
    ]


def print_points(points):
    for point in points:
        print(f"- {point['summary']}")


@pytest.mark.parametrize("posting", [
    swe_posting,
    ml_posting,
    embedded_posting,
    cloud_posting,
    startup_posting,
    big_company_posting
])
def test_rank_different_points(posting, very_different_points):
    posting = JobPosting(posting())
    
    print_points(
        top_k_points(posting, very_different_points)
    )


@pytest.mark.parametrize("posting", [
    swe_posting,
    ml_posting,
    embedded_posting,
    cloud_posting,
    startup_posting,
    big_company_posting
])
def test_rank_similar_points(posting, very_similar_points):
    posting = JobPosting(posting())
    
    print_points(
        top_k_points(posting, very_similar_points)
    )


@pytest.mark.parametrize("posting", [
    swe_posting,
    ml_posting,
])
def test_rank_ml_points(posting, ml_and_swe_points):
    posting = JobPosting(posting())
    
    print_points(
        top_k_points(posting, ml_and_swe_points)
    )


@pytest.mark.parametrize("posting", [
    startup_posting,
    big_company_posting
])
def test_rank_leadership_points(posting, leadership_independence_points):
    posting = JobPosting(posting())
    
    print_points(
        top_k_points(posting, leadership_independence_points)
    )


@pytest.mark.parametrize("posting", [
    swe_posting,
    ml_posting,
    embedded_posting,
    cloud_posting,
    startup_posting,
    big_company_posting
])
def test_keywords(posting):
    posting = JobPosting(posting())
    
    print(posting.keywords)
