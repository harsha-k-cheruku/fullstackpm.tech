from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CourseExplainer:
    name: str
    slug: str
    family: str
    overview: str
    who_this_fits: str
    eli10: str
    school_connection: str
    reality_check: str
    choose_if: str
    avoid_if: str
    what_you_study: list[str]
    problems_and_work: list[str]
    roles: list[str]
    tradeoffs: list[str]
    good_fit_checklist: list[str]
    misconceptions: list[str]
    example_projects: list[str]
    similar_branches: list[str]
    year_by_year: list = None  # list of dicts: {year, theme, courses: [{name, teaches, tests}]}


TOP_12_COURSES: list[CourseExplainer] = [
    CourseExplainer(
        name="Computer Science and Engineering",
        slug="computer-science-and-engineering",
        family="computing",
        overview="The broadest software-oriented engineering branch. You learn to build software systems, reason about algorithms, design architectures, and work across the full stack of digital product development — from mobile apps to distributed backends to ML pipelines.",
        who_this_fits="students who genuinely enjoy coding, logic, abstraction, and building digital things — not just students who heard it pays well",
        eli10="You learn how computers think, how software gets built, and how to make apps, tools, and systems that solve real problems. If you have ever wondered how YouTube recommends videos or how Google Maps finds the fastest route — that is the kind of thinking CSE teaches you.",
        school_connection="If you liked mathematics (especially logic, sets, and problem-solving puzzles) and enjoyed writing code or tinkering with computers, CSE extends that into serious engineering.",
        reality_check="CSE creates enormous opportunity, but it also attracts enormous crowds. If you do not actually enjoy sitting with code for hours, debugging patiently, and learning new tools constantly — the hype wears off fast and you are left competing in the most crowded lane with people who do enjoy it.",
        choose_if="Choose CSE if you want the widest software career flexibility and genuinely like solving problems through code, system design, and logical reasoning.",
        avoid_if="Avoid CSE if you are choosing it only because relatives said it is the safest option, while you secretly find debugging tedious and would rather work with physical systems or science.",
        what_you_study=[
            "Programming fundamentals, data structures, algorithms — the bread and butter of every technical interview and real engineering role",
            "Operating systems, databases, computer networks, and compilers — how the layers under your code actually work",
            "Software engineering, system design, and architecture — how real products get built at scale",
            "Math foundations: discrete math, probability, linear algebra — not for decoration, but because they power optimization, ML, and systems thinking",
            "Electives like AI/ML, cybersecurity, distributed systems, or graphics depending on your interest and college",
        ],
        problems_and_work=[
            "Building web apps, mobile apps, APIs, microservices, and product backends",
            "Designing systems that handle millions of users without falling over at 2 AM",
            "Writing code that other engineers can read, maintain, and extend — not just code that runs once",
            "Debugging performance bottlenecks, fixing production incidents, and improving developer tooling",
            "Working on data pipelines, recommendation systems, search engines, or internal business tools",
        ],
        roles=[
            "Software Engineer — the most common and flexible starting point",
            "Backend / Full-Stack Engineer — building the server-side brains of products",
            "Platform or Infrastructure Engineer — building the systems that other engineers depend on",
            "ML Engineer — applying machine learning to real product problems",
            "DevOps / SRE — keeping systems reliable, fast, and safe at scale",
        ],
        tradeoffs=[
            "The branch is absurdly competitive because half the country wants in — standing out requires actual skill, not just the degree",
            "Your degree opens doors, but projects, internships, and problem-solving depth decide whether you walk through them",
            "Tech changes fast — if you stop learning after college, you fall behind within 2–3 years",
            "Remote work is common but so is burnout culture in high-pressure engineering orgs",
        ],
        good_fit_checklist=[
            "I enjoy coding even when it becomes frustrating and the bug does not make sense",
            "I like logic, structured thinking, and breaking big problems into smaller pieces",
            "I want broad digital career flexibility across industries",
            "I am okay with constant upskilling — learning never really stops in this field",
            "I find building things with code more satisfying than just studying theory",
        ],
        misconceptions=[
            "\"CSE guarantees a high-paying job.\" — It guarantees access to a crowded market. Your execution decides the outcome.",
            "\"You need to be a genius coder from age 12.\" — Most successful engineers learned properly in college. Starting point matters less than consistency.",
            "\"CSE = only coding.\" — Real software engineering involves system design, communication, debugging, and understanding user problems, not just typing code.",
            "\"IIT CSE is the only version worth doing.\" — College quality matters, but a motivated student at a good NIT or IIIT can outperform a drifting student at a top IIT.",
        ],
        example_projects=[
            "Building a food delivery app backend that handles real-time order tracking and payment processing",
            "Designing a recommendation engine that suggests products based on browsing history",
            "Creating an internal dashboard that helps a business team track KPIs without asking engineering every time",
            "Writing a distributed cache system that speeds up database reads by 10x for a high-traffic site",
            "Building a CI/CD pipeline that automatically tests and deploys code changes safely",
        ],
        similar_branches=["Information Technology", "Mathematics and Computing", "Electronics and Communication Engineering"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and first taste of code",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, linear algebra, differential equations \u2014 the math that powers algorithms and optimization later",
                                        "tests": "Written exams heavy on problem solving; expect proofs and derivations"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Mechanics, waves, optics, and basic quantum concepts \u2014 general science foundation",
                                        "tests": "Theory exams plus physics lab practicals with viva"
                                },
                                {
                                        "name": "Introduction to Programming",
                                        "teaches": "Variables, loops, functions, arrays, basic problem solving in C or Python",
                                        "tests": "Lab exams where you write and run code under time pressure; written exam on logic"
                                },
                                {
                                        "name": "Basic Electrical/Electronics",
                                        "teaches": "Circuit fundamentals, signals, and digital logic basics \u2014 cross-disciplinary exposure",
                                        "tests": "Circuit analysis problems and simple lab experiments"
                                },
                                {
                                        "name": "Engineering Drawing / Workshop",
                                        "teaches": "Technical sketching, orthographic projections, and basic manufacturing processes",
                                        "tests": "Drawing sheets graded on precision; workshop evaluation on completed items"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Core CS fundamentals \u2014 data structures, logic, and how computers work inside",
                        "courses": [
                                {
                                        "name": "Data Structures",
                                        "teaches": "Arrays, linked lists, stacks, queues, trees, graphs, hashing \u2014 how data gets organized for efficient access",
                                        "tests": "Coding assignments, lab exams implementing structures, written exams on complexity analysis"
                                },
                                {
                                        "name": "Discrete Mathematics",
                                        "teaches": "Sets, relations, graph theory, combinatorics, logic \u2014 the math backbone of computer science",
                                        "tests": "Proof-based written exams; problem sets that test formal reasoning"
                                },
                                {
                                        "name": "Digital Logic Design",
                                        "teaches": "Boolean algebra, gates, flip-flops, counters, basic processor architecture concepts",
                                        "tests": "Design problems on paper plus digital circuit lab experiments"
                                },
                                {
                                        "name": "Object-Oriented Programming",
                                        "teaches": "Classes, inheritance, polymorphism, design patterns \u2014 writing modular, reusable code",
                                        "tests": "Coding projects, lab exams building OOP systems, written theory on design principles"
                                },
                                {
                                        "name": "Computer Organization & Architecture",
                                        "teaches": "How CPUs execute instructions, memory hierarchy, pipelining, assembly language basics",
                                        "tests": "Written exams on architecture concepts; assembly programming assignments"
                                },
                                {
                                        "name": "Database Management Systems",
                                        "teaches": "SQL, relational models, normalization, indexing, transactions \u2014 how data gets stored and queried",
                                        "tests": "SQL lab exams, database design projects, written theory on normalization and transactions"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Systems depth \u2014 operating systems, networks, algorithms, and software engineering",
                        "courses": [
                                {
                                        "name": "Operating Systems",
                                        "teaches": "Process management, memory management, file systems, concurrency \u2014 how your code actually runs on hardware",
                                        "tests": "Written exams on scheduling and memory; coding assignments implementing OS concepts"
                                },
                                {
                                        "name": "Computer Networks",
                                        "teaches": "TCP/IP, routing, HTTP, DNS, sockets \u2014 how machines communicate across the internet",
                                        "tests": "Packet analysis labs, network programming assignments, protocol-heavy written exams"
                                },
                                {
                                        "name": "Design and Analysis of Algorithms",
                                        "teaches": "Divide-and-conquer, dynamic programming, greedy algorithms, NP-completeness, complexity classes",
                                        "tests": "Algorithm design problems on paper; coding contests; complexity proofs"
                                },
                                {
                                        "name": "Software Engineering",
                                        "teaches": "SDLC, requirements, testing, agile, version control \u2014 how real teams build and ship software",
                                        "tests": "Group project building a working application; written exam on methodologies"
                                },
                                {
                                        "name": "Compiler Design",
                                        "teaches": "Lexical analysis, parsing, code generation \u2014 how programming languages get translated to machine code",
                                        "tests": "Building a mini-compiler as a project; written exams on grammar and parsing theory"
                                },
                                {
                                        "name": "Theory of Computation",
                                        "teaches": "Automata, formal languages, Turing machines, computability \u2014 what can and cannot be computed",
                                        "tests": "Proof-heavy written exams; formal language construction problems"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Specialization, electives, and capstone project",
                        "courses": [
                                {
                                        "name": "Machine Learning / AI (elective)",
                                        "teaches": "Regression, classification, neural networks, model evaluation \u2014 making predictions from data",
                                        "tests": "ML project with real dataset; written exam on algorithms and math foundations"
                                },
                                {
                                        "name": "Distributed Systems (elective)",
                                        "teaches": "Consensus, replication, fault tolerance, MapReduce \u2014 how large-scale systems work",
                                        "tests": "System design assignments; written exam on distributed algorithms"
                                },
                                {
                                        "name": "Information Security (elective)",
                                        "teaches": "Cryptography, authentication, network security, ethical hacking basics",
                                        "tests": "Security analysis labs; written exam on crypto protocols and threat models"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "End-to-end engineering: problem identification, design, implementation, testing, and presentation",
                                        "tests": "Project demo, written report, viva voce with external examiner"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Mechanical Engineering",
        slug="mechanical-engineering",
        family="mechanical",
        overview="The branch of machines, motion, manufacturing, thermal systems, robotics, and physical product design. One of the oldest and broadest engineering disciplines — relevant everywhere from automotive to aerospace to consumer products to energy.",
        who_this_fits="students who like machines, mechanisms, physical products, and want to see engineering become tangible — not just pixels on a screen",
        eli10="You learn how machines move, how engines work, how things get manufactured, and how to design products that survive real-world forces. If you have ever taken apart a toy to see how it works — Mechanical Engineering is that curiosity turned into a career.",
        school_connection="If you liked physics (especially mechanics and thermodynamics) and enjoyed understanding how machines, engines, or physical systems work, Mechanical extends that into design, manufacturing, and real-world problem solving.",
        reality_check="Mechanical Engineering is not 'outdated.' It is foundational. But students often expect prestige to carry them, when the branch actually rewards hands-on depth, internships, CAD/simulation skills, and specialization. The generic ME degree is broad — your direction within it matters a lot.",
        choose_if="Choose Mechanical if you enjoy physical systems, product design, manufacturing, robotics, or understanding how real machines and products behave under stress.",
        avoid_if="Avoid Mechanical if you only want a laptop-only career and have no interest in factories, hardware, physical products, or industrial systems.",
        what_you_study=[
            "Engineering mechanics, thermodynamics, fluid mechanics, and heat transfer — the physics backbone of the branch",
            "Machine design, mechanisms, and kinematics — how to design components that actually work under load",
            "Manufacturing processes — casting, machining, welding, 3D printing, and how real products get made",
            "Materials science basics — why steel behaves differently from aluminum and when it matters",
            "CAD/CAM, FEA simulation, and computational tools used in modern mechanical design",
            "Electives in robotics, automotive engineering, energy systems, or industrial automation depending on college",
        ],
        problems_and_work=[
            "Designing automotive components that meet safety, weight, and cost targets simultaneously",
            "Optimizing manufacturing processes to reduce waste, defects, and production time",
            "Running stress analysis and thermal simulations on parts before they ever get built",
            "Working on HVAC systems, power plants, or energy infrastructure",
            "Testing prototypes, validating designs against real-world loads, and iterating based on failure modes",
            "Managing production lines, quality processes, and supply chain coordination in manufacturing",
        ],
        roles=[
            "Design Engineer — creating components, assemblies, and product designs in CAD",
            "Manufacturing Engineer — optimizing how things get built in factories",
            "Automotive Engineer — working on vehicles, powertrains, or EV systems",
            "Production/Operations Engineer — managing factory output, quality, and efficiency",
            "R&D Engineer — developing new products, materials, or processes",
            "Robotics Engineer — designing and building mechanical systems for automation",
        ],
        tradeoffs=[
            "Core roles can be more location-dependent than software — factories are not in every city",
            "You need internships, CAD skills, and domain exposure to stand out — the generic degree is not enough",
            "Some roles are execution-heavy and physically demanding, not just desk work",
            "Starting salaries may be lower than software, but ceiling depends heavily on specialization and industry",
        ],
        good_fit_checklist=[
            "I enjoy physical systems and products more than purely digital work",
            "I like understanding how things move, break, and get manufactured",
            "I can handle practical constraints and messy real-world engineering problems",
            "I can see myself in factories, labs, test facilities, or product design offices",
            "I find building or fixing physical things satisfying",
        ],
        misconceptions=[
            "\"Mechanical is old-fashioned and dying.\" — Mechanical engineers work on EVs, robotics, drones, renewable energy, and advanced manufacturing. The field keeps evolving.",
            "\"You will only work in dirty factories.\" — Many roles are in R&D labs, design offices, or tech companies that make physical products.",
            "\"Software pays more, so Mechanical is a bad choice.\" — If you hate software but love machines, forcing yourself into CSE is worse for your career than picking ME and excelling.",
            "\"All ME graduates do the same work.\" — The branch is enormously broad. An automotive design engineer and a manufacturing process engineer have very different daily lives.",
        ],
        example_projects=[
            "Designing a suspension system for an electric vehicle that balances ride comfort with handling",
            "Setting up and optimizing a CNC machining process for aerospace-grade turbine blades",
            "Running CFD simulations to improve airflow in a data center cooling system",
            "Building a robotic arm prototype for a college competition or startup",
            "Analyzing why a specific component keeps failing in the field and redesigning it to last 3x longer",
        ],
        similar_branches=["Industrial Engineering", "Aerospace Engineering", "Civil Engineering"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and engineering basics",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, linear algebra, differential equations, vector calculus \u2014 math for mechanical analysis",
                                        "tests": "Written exams with problem solving; emphasis on applied calculation"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Mechanics, thermodynamics basics, waves, properties of matter \u2014 physics foundations for ME",
                                        "tests": "Theory exams plus lab practicals with measurement experiments"
                                },
                                {
                                        "name": "Engineering Chemistry",
                                        "teaches": "Material properties, corrosion, fuels, polymers \u2014 chemistry relevant to manufacturing and materials",
                                        "tests": "Written exam plus chemistry lab practical and viva"
                                },
                                {
                                        "name": "Engineering Drawing & CAD",
                                        "teaches": "Orthographic projections, sections, isometric views, basic AutoCAD \u2014 communicating designs visually",
                                        "tests": "Drawing sheet exams graded on accuracy and standards compliance"
                                },
                                {
                                        "name": "Workshop Practice",
                                        "teaches": "Fitting, welding, carpentry, casting, machining basics \u2014 hands-on manufacturing experience",
                                        "tests": "Completed workshop pieces evaluated for precision and finish"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Core mechanics \u2014 forces, materials, fluids, and thermal science",
                        "courses": [
                                {
                                        "name": "Engineering Mechanics / Statics & Dynamics",
                                        "teaches": "Force analysis, equilibrium, kinematics, work-energy methods \u2014 how forces act on structures and machines",
                                        "tests": "Numerical problem-heavy written exams; free body diagram analysis"
                                },
                                {
                                        "name": "Strength of Materials",
                                        "teaches": "Stress, strain, bending, torsion, deflection \u2014 how components deform and fail under load",
                                        "tests": "Numerical problems on beams and shafts; lab experiments with UTM and strain gauges"
                                },
                                {
                                        "name": "Thermodynamics",
                                        "teaches": "Laws of thermodynamics, cycles, entropy, work-heat relationships \u2014 energy analysis fundamentals",
                                        "tests": "Cycle analysis problems; written exams heavy on first and second law applications"
                                },
                                {
                                        "name": "Fluid Mechanics",
                                        "teaches": "Fluid statics, Bernoulli's equation, viscous flow, dimensional analysis \u2014 how fluids behave in systems",
                                        "tests": "Numerical problem exams; hydraulics lab measuring flow and pressure"
                                },
                                {
                                        "name": "Manufacturing Processes",
                                        "teaches": "Casting, forming, machining, joining \u2014 how raw materials become finished components",
                                        "tests": "Theory exam on process selection; lab reports on manufacturing experiments"
                                },
                                {
                                        "name": "Material Science",
                                        "teaches": "Crystal structures, phase diagrams, mechanical properties, heat treatment \u2014 why materials behave differently",
                                        "tests": "Written exam on structure-property relationships; metallography lab"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Design, thermal systems, and industrial applications",
                        "courses": [
                                {
                                        "name": "Machine Design",
                                        "teaches": "Shaft design, gear design, bearing selection, fatigue analysis \u2014 designing components that survive real loads",
                                        "tests": "Design problems requiring calculations and factor-of-safety decisions; design project"
                                },
                                {
                                        "name": "Heat Transfer",
                                        "teaches": "Conduction, convection, radiation, heat exchangers \u2014 how thermal energy moves through systems",
                                        "tests": "Numerical problems on heat transfer modes; lab experiments with heat exchangers"
                                },
                                {
                                        "name": "Dynamics of Machinery",
                                        "teaches": "Mechanisms, cams, governors, balancing, vibrations \u2014 how machines move and how to control motion",
                                        "tests": "Mechanism analysis problems; vibration measurement lab experiments"
                                },
                                {
                                        "name": "CAD/CAM & FEA",
                                        "teaches": "3D modeling in SolidWorks/CATIA, computer-aided manufacturing, finite element basics",
                                        "tests": "CAD modeling assignments; FEA simulation project; lab practical exam"
                                },
                                {
                                        "name": "Industrial Engineering",
                                        "teaches": "Operations research, quality control, production planning, work study \u2014 factory-level optimization",
                                        "tests": "Linear programming and scheduling problems; case study analysis"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Specialization, advanced topics, and capstone",
                        "courses": [
                                {
                                        "name": "Automobile Engineering (elective)",
                                        "teaches": "Vehicle dynamics, powertrain, suspension, braking systems \u2014 how cars and trucks are engineered",
                                        "tests": "Design analysis assignments; written exam on vehicle subsystems"
                                },
                                {
                                        "name": "Robotics (elective)",
                                        "teaches": "Robot kinematics, dynamics, sensors, actuators, control \u2014 designing machines that move intelligently",
                                        "tests": "Robot simulation project; written exam on kinematics and control"
                                },
                                {
                                        "name": "Finite Element Analysis (elective)",
                                        "teaches": "Meshing, boundary conditions, stress-strain simulation \u2014 predicting how designs behave before building them",
                                        "tests": "FEA simulation project with analysis report; written exam on FEM theory"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "End-to-end design project: problem definition, analysis, prototyping, testing, and documentation",
                                        "tests": "Working prototype or simulation demo, written report, viva voce"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Electronics and Communication Engineering",
        slug="electronics-and-communication-engineering",
        family="electronics",
        overview="A strong hybrid branch covering circuits, signal processing, communication systems, embedded devices, and the hardware-software interface. ECE sits at the intersection of physical electronics and digital systems.",
        who_this_fits="students who like electronics, signals, embedded systems, and want flexibility across hardware, telecom, semiconductor, and software-adjacent paths",
        eli10="You learn how phones talk to cell towers, how chips inside devices work, how signals carry information, and how to design the electronic systems that power everything from WiFi routers to satellites. If you have ever wondered how Bluetooth works — ECE is where you find out.",
        school_connection="If you liked physics (especially electricity and magnetism) and enjoyed tinkering with circuits, Arduino, or electronics projects, ECE takes that curiosity into serious engineering territory.",
        reality_check="ECE is one of the most misunderstood branches. Students pick it expecting 'CSE-lite' and then get surprised by signal processing math, analog circuits, and electromagnetic theory. It is genuinely versatile — but the versatility comes from depth, not from dodging the hard parts.",
        choose_if="Choose ECE if you want hardware depth while keeping doors open to embedded systems, semiconductor work, telecom, VLSI, and even software roles later.",
        avoid_if="Avoid ECE if you dislike circuits, math-heavy engineering, and are only picking it because it sounds close enough to CSE without being CSE.",
        what_you_study=[
            "Analog and digital circuits, electronic devices, and semiconductor physics — how real hardware works at the component level",
            "Signals and systems, digital signal processing, and communication theory — how information gets encoded, transmitted, and decoded",
            "Embedded systems, microcontrollers, and FPGA-based design — programming hardware directly",
            "Electromagnetic theory and antenna design — the physics behind wireless communication",
            "Control systems — how systems self-regulate and respond to feedback",
            "Electives in VLSI design, IoT, wireless networks, or image processing depending on interest",
        ],
        problems_and_work=[
            "Designing circuits for consumer electronics, medical devices, or industrial equipment",
            "Building embedded firmware for IoT devices, automotive electronics, or smart hardware",
            "Working on semiconductor chip design (VLSI), layout, and verification",
            "Developing communication protocols and testing wireless system performance",
            "Writing signal processing algorithms for audio, image, radar, or biomedical applications",
            "Testing and validating electronic products against safety and performance standards",
        ],
        roles=[
            "Embedded Systems Engineer — writing firmware and designing hardware-software interfaces",
            "VLSI / Chip Design Engineer — designing or verifying semiconductor circuits",
            "Signal Processing Engineer — working on audio, radar, communications, or imaging systems",
            "Telecom / RF Engineer — designing and optimizing wireless communication systems",
            "Hardware Design Engineer — creating circuit boards and electronic products",
            "Software Engineer — many ECE graduates transition into software with a systems-thinking edge",
        ],
        tradeoffs=[
            "The branch is harder than students expect because it mixes abstraction, math, and physical hardware constraints",
            "Core ECE roles (VLSI, embedded, RF) often need more specialization than generic software placement tracks",
            "Many students drift into software not by choice but because they never built confidence in the electronics side — which wastes the branch's real strength",
            "Lab work matters — you learn electronics by building, not just by solving equations in a notebook",
        ],
        good_fit_checklist=[
            "I like circuits, signals, or electronic devices — not just in theory, but in practice",
            "I am comfortable with serious math in engineering (transforms, complex analysis, probability)",
            "I want flexibility between hardware-facing and software-adjacent career paths",
            "I care about how systems work underneath the interface layer — not just the app on top",
            "I have some patience for lab work and debugging hardware, which is slower and messier than software debugging",
        ],
        misconceptions=[
            "\"ECE is just CSE with extra steps.\" — No. ECE is a different branch with different core skills. The overlap exists but the foundations are distinct.",
            "\"Everyone in ECE ends up in software anyway.\" — Many do, but the ones who stay in core ECE (VLSI, embedded, RF) often have less competition and strong career depth.",
            "\"You don't need lab skills for ECE.\" — You really do. The branch clicks when you build circuits, not just analyze them on paper.",
            "\"ECE is dying because software is eating the world.\" — Software runs on hardware. Semiconductors, 5G, IoT, and EV electronics are booming fields, and they need ECE graduates.",
        ],
        example_projects=[
            "Designing an embedded system that reads sensor data and controls a motor in real-time",
            "Building a Bluetooth Low Energy (BLE) device that communicates with a mobile app",
            "Designing a VLSI circuit block for a specific function like a multiplier or memory controller",
            "Implementing a digital filter that cleans noise from audio or biomedical signals",
            "Testing a PCB prototype for signal integrity, power consumption, and thermal performance",
        ],
        similar_branches=["Electrical Engineering", "Electrical and Electronics Engineering", "Information Technology"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and introduction to circuits",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, linear algebra, complex analysis, transforms \u2014 math essential for signal and circuit analysis",
                                        "tests": "Written exams with heavy emphasis on transforms and complex variable problems"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Electromagnetic waves, optics, quantum physics basics, semiconductor physics introduction",
                                        "tests": "Theory exams plus optics and semiconductor lab experiments"
                                },
                                {
                                        "name": "Basic Electrical Engineering",
                                        "teaches": "Circuit laws, AC/DC analysis, transformers, basic machines \u2014 electrical fundamentals for ECE",
                                        "tests": "Circuit analysis problems and basic electrical lab experiments"
                                },
                                {
                                        "name": "Introduction to Programming",
                                        "teaches": "C programming, logic building, functions, arrays \u2014 coding fundamentals for embedded systems later",
                                        "tests": "Lab exams with timed coding; written exam on programming logic"
                                },
                                {
                                        "name": "Engineering Drawing / Workshop",
                                        "teaches": "Technical drawing, basic manufacturing processes, soldering practice",
                                        "tests": "Drawing sheets and workshop practical evaluation"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Core electronics \u2014 circuits, devices, signals, and digital systems",
                        "courses": [
                                {
                                        "name": "Network Theory",
                                        "teaches": "KVL, KCL, mesh/nodal analysis, transient response, network theorems \u2014 systematic circuit solving",
                                        "tests": "Heavy numerical problems on circuit analysis; lab verification of theorems"
                                },
                                {
                                        "name": "Electronic Devices & Circuits",
                                        "teaches": "Diodes, BJTs, FETs, amplifier circuits, biasing \u2014 how individual electronic components work",
                                        "tests": "Circuit design problems; electronics lab building amplifier circuits on breadboards"
                                },
                                {
                                        "name": "Signals and Systems",
                                        "teaches": "Fourier transforms, Laplace transforms, convolution, system response \u2014 mathematical framework for signals",
                                        "tests": "Transform-heavy written exams; MATLAB/Python signal analysis assignments"
                                },
                                {
                                        "name": "Digital Electronics",
                                        "teaches": "Boolean algebra, combinational and sequential circuits, flip-flops, counters, basic FPGA concepts",
                                        "tests": "Logic design problems; digital lab building circuits on trainer kits"
                                },
                                {
                                        "name": "Electromagnetic Theory",
                                        "teaches": "Maxwell's equations, wave propagation, transmission lines, antenna basics \u2014 the physics of wireless",
                                        "tests": "Derivation-heavy written exam; EM field simulation assignments"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Communication systems, embedded, and advanced electronics",
                        "courses": [
                                {
                                        "name": "Communication Systems",
                                        "teaches": "Analog and digital modulation, noise analysis, channel capacity, wireless system design",
                                        "tests": "Modulation analysis problems; communication lab with signal generators and analyzers"
                                },
                                {
                                        "name": "Microprocessors & Microcontrollers",
                                        "teaches": "8085/ARM architecture, assembly programming, interfacing peripherals \u2014 programming hardware directly",
                                        "tests": "Assembly coding lab exams; interfacing project with sensors and displays"
                                },
                                {
                                        "name": "Control Systems",
                                        "teaches": "Transfer functions, stability analysis, Bode plots, PID controllers \u2014 how systems self-regulate",
                                        "tests": "Stability analysis problems; control lab with servo motor experiments"
                                },
                                {
                                        "name": "Analog Circuit Design",
                                        "teaches": "Op-amp circuits, oscillators, filters, power supplies \u2014 designing real analog electronic systems",
                                        "tests": "Circuit design assignments; analog lab building and testing functional circuits"
                                },
                                {
                                        "name": "Digital Signal Processing",
                                        "teaches": "DFT, FFT, FIR/IIR filters, spectral analysis \u2014 processing signals digitally for real applications",
                                        "tests": "Filter design projects; DSP lab using MATLAB or DSP hardware kits"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Specialization, advanced systems, and capstone",
                        "courses": [
                                {
                                        "name": "VLSI Design (elective)",
                                        "teaches": "CMOS circuit design, layout, verification, ASIC flow \u2014 designing chips at the transistor level",
                                        "tests": "VLSI design project using Cadence/Synopsis tools; written exam on CMOS theory"
                                },
                                {
                                        "name": "Wireless Communication (elective)",
                                        "teaches": "Fading channels, OFDM, MIMO, cellular systems, 4G/5G concepts",
                                        "tests": "System analysis problems; simulation project on wireless channel performance"
                                },
                                {
                                        "name": "Embedded Systems (elective)",
                                        "teaches": "Real-time OS, embedded C, hardware-software co-design, IoT device development",
                                        "tests": "Embedded system project with working hardware; code review and demo"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "End-to-end hardware/software project: design, prototype, test, and defend",
                                        "tests": "Working demo, project report, external examiner viva"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Civil Engineering",
        slug="civil-engineering",
        family="civil",
        overview="The branch behind infrastructure: roads, bridges, buildings, water supply, transportation, and the physical backbone of cities and civilizations. Everything you see when you look out of a car window was touched by civil engineering.",
        who_this_fits="students who want visible, large-scale, real-world impact — building things that last decades and serve millions of people",
        eli10="You help design the things cities are made of — buildings, roads, bridges, water systems, and transport networks. Next time you cross a bridge and it does not collapse, thank a civil engineer.",
        school_connection="If you liked physics (especially mechanics and forces) and found yourself noticing buildings, construction sites, or infrastructure projects, Civil Engineering turns that awareness into an actual profession.",
        reality_check="Civil Engineering often gets dismissed online because it is less glamorous than tech. But it is one of the few branches where your work is literally visible for decades. The key question is whether you actually want infrastructure work, site realities, and long project cycles — not whether the branch is 'good enough.'",
        choose_if="Choose Civil if you care about structures, infrastructure, urban systems, construction, and physical engineering with visible, lasting impact.",
        avoid_if="Avoid Civil if you need everything to be fast, remote, digitally abstract, and you cannot tolerate site visits, dust, or real-world execution messiness.",
        what_you_study=[
            "Structural engineering — how buildings and bridges resist loads without collapsing",
            "Geotechnical engineering — how soil and rock behave under foundations and structures",
            "Transportation engineering — how roads, highways, and transit networks get planned and designed",
            "Water resources and environmental engineering — how cities manage water supply, drainage, and treatment",
            "Construction management — how large projects get planned, estimated, scheduled, and executed",
            "Surveying, concrete technology, and materials testing — the practical tools of the field",
        ],
        problems_and_work=[
            "Designing foundations, columns, beams, and slabs for multi-story buildings",
            "Planning road networks, intersections, and traffic flow for growing cities",
            "Managing construction projects — coordinating labor, materials, equipment, timelines, and budgets",
            "Designing water distribution systems, sewage networks, and flood management solutions",
            "Evaluating structural safety of existing buildings and bridges, especially after earthquakes or aging",
            "Running geotechnical investigations before any major construction begins",
        ],
        roles=[
            "Structural Engineer — designing buildings, bridges, and load-bearing systems",
            "Site / Construction Engineer — managing execution on real construction projects",
            "Transportation Engineer — planning and designing roads, transit, and urban mobility",
            "Water Resources Engineer — designing supply, drainage, and treatment systems",
            "Geotechnical Engineer — analyzing soil and foundation behavior for construction",
            "Project Manager — coordinating large infrastructure projects end-to-end",
        ],
        tradeoffs=[
            "Many roles involve site visits, fieldwork, and physical environments — this is not fully remote-friendly",
            "Career growth often depends on execution experience and professional certifications, not just academic marks",
            "Projects can take years — if you need instant gratification, this field tests your patience",
            "Public perception undervalues the branch, but actual demand for infrastructure engineering is enormous",
        ],
        good_fit_checklist=[
            "I care about physical infrastructure and the built environment around me",
            "I can handle practical constraints, long timelines, and real-world project messiness",
            "I do not need a fully laptop-only career to feel successful",
            "I find visible, lasting, real-world impact genuinely motivating",
            "I can see myself working on construction sites, in design offices, or with government infrastructure teams",
        ],
        misconceptions=[
            "\"Civil Engineering has no scope.\" — India literally needs trillions of rupees of infrastructure investment. The scope is enormous, even if LinkedIn does not celebrate it.",
            "\"You will only build houses.\" — Civil covers bridges, tunnels, highways, airports, dams, water systems, and urban planning. The range is wider than most students realize.",
            "\"It is only a government job branch.\" — Private construction, consulting, real estate development, and infrastructure companies all hire civil engineers actively.",
            "\"Civil engineers cannot earn well.\" — Experienced structural consultants, project managers, and infrastructure specialists earn very well. The path is just different from software's immediate salary ramp.",
        ],
        example_projects=[
            "Designing the structural frame for a 15-story residential building to withstand earthquake loads",
            "Planning a new highway interchange that reduces traffic bottlenecks in a growing city",
            "Building a water treatment plant that serves 100,000 people with safe drinking water",
            "Conducting soil testing and foundation design for a new metro rail station",
            "Managing a bridge construction project from tender to completion in 18 months",
        ],
        similar_branches=["Mechanical Engineering", "Environmental Engineering", "Architecture-adjacent planning paths"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and engineering basics",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, linear algebra, numerical methods \u2014 math for structural and hydraulic analysis",
                                        "tests": "Written exams; emphasis on applied numerical problem solving"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Mechanics, waves, properties of matter \u2014 physics foundation for structural understanding",
                                        "tests": "Theory exam plus physics lab practicals"
                                },
                                {
                                        "name": "Engineering Chemistry",
                                        "teaches": "Water chemistry, construction materials, corrosion \u2014 chemistry relevant to civil infrastructure",
                                        "tests": "Written exam plus chemistry lab focused on water testing"
                                },
                                {
                                        "name": "Engineering Drawing",
                                        "teaches": "Projection systems, sections, building plan basics \u2014 visual communication for civil design",
                                        "tests": "Drawing sheet exams evaluated for accuracy and drafting standards"
                                },
                                {
                                        "name": "Introduction to Civil Engineering",
                                        "teaches": "Overview of structures, transportation, water resources, construction \u2014 branch orientation",
                                        "tests": "Introductory exam plus site visit reports"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Core mechanics \u2014 structures, soil, fluids, and surveying",
                        "courses": [
                                {
                                        "name": "Strength of Materials",
                                        "teaches": "Stress-strain, bending moments, shear force diagrams, column buckling \u2014 how structural members behave",
                                        "tests": "Numerical problems on beams and columns; lab testing concrete and steel specimens"
                                },
                                {
                                        "name": "Surveying",
                                        "teaches": "Chain, compass, theodolite, total station, GPS surveying \u2014 measuring land accurately for construction",
                                        "tests": "Field surveying practicals with instrument handling; computation assignments"
                                },
                                {
                                        "name": "Fluid Mechanics & Hydraulics",
                                        "teaches": "Fluid statics, pipe flow, open channel flow, dimensional analysis \u2014 water behavior in systems",
                                        "tests": "Numerical problem exams; hydraulics lab measuring flow rates and pressures"
                                },
                                {
                                        "name": "Building Materials & Construction",
                                        "teaches": "Concrete, steel, bricks, timber, modern materials \u2014 properties, testing, and construction techniques",
                                        "tests": "Material testing lab (cube testing, slump test); written exam on specifications"
                                },
                                {
                                        "name": "Engineering Geology",
                                        "teaches": "Rock types, soil formation, geological mapping, groundwater \u2014 understanding the ground you build on",
                                        "tests": "Geological specimen identification; field report on local geology"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Design and analysis \u2014 structures, geotechnical, transportation",
                        "courses": [
                                {
                                        "name": "Structural Analysis",
                                        "teaches": "Determinate and indeterminate structures, matrix methods, influence lines \u2014 analyzing how forces flow",
                                        "tests": "Complex structural analysis problems; computer-aided analysis assignments"
                                },
                                {
                                        "name": "Design of Concrete Structures",
                                        "teaches": "RCC beam, slab, column, and footing design using IS codes \u2014 designing real structural elements",
                                        "tests": "Design problems applying IS 456 code provisions; mini design project"
                                },
                                {
                                        "name": "Geotechnical Engineering",
                                        "teaches": "Soil classification, shear strength, consolidation, bearing capacity \u2014 understanding foundation behavior",
                                        "tests": "Soil testing lab (triaxial, consolidation tests); foundation design problems"
                                },
                                {
                                        "name": "Transportation Engineering",
                                        "teaches": "Highway geometry, pavement design, traffic engineering, railway basics \u2014 designing movement systems",
                                        "tests": "Highway design project; traffic survey fieldwork; written exam on design standards"
                                },
                                {
                                        "name": "Water Resources Engineering",
                                        "teaches": "Hydrology, irrigation, dam design, flood estimation \u2014 managing water for human use",
                                        "tests": "Hydrological analysis problems; dam/canal design assignments"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Advanced design, management, and capstone",
                        "courses": [
                                {
                                        "name": "Design of Steel Structures",
                                        "teaches": "Tension members, compression members, connections, beam-column design using IS 800",
                                        "tests": "Steel design problems applying code provisions; structural design project"
                                },
                                {
                                        "name": "Construction Project Management",
                                        "teaches": "Planning, scheduling (CPM/PERT), estimation, contracts, quality management \u2014 running real projects",
                                        "tests": "Project scheduling assignments; quantity estimation exercises; case study analysis"
                                },
                                {
                                        "name": "Environmental Engineering",
                                        "teaches": "Water treatment, wastewater treatment, solid waste management, air pollution control",
                                        "tests": "Treatment plant design problems; environmental lab testing water quality"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "Complete civil engineering project: site investigation, design, analysis, drawings, and presentation",
                                        "tests": "Design drawings, analysis report, project defense with external examiner"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Electrical Engineering",
        slug="electrical-engineering",
        family="electronics",
        overview="Power systems, electrical machines, control systems, energy infrastructure, and the engineering of how electricity gets generated, transmitted, distributed, and used. This is the branch that keeps the lights on — literally.",
        who_this_fits="students who like power, energy, control systems, machines, and mathematically rigorous engineering with real infrastructure impact",
        eli10="You learn how electricity gets made in power plants, travels through wires, and runs everything from factory motors to your home appliances. Without electrical engineers, the entire grid falls apart.",
        school_connection="If you liked physics (especially current, magnetism, and circuit problems) and found power systems or electrical machines interesting rather than boring, Electrical Engineering takes that directly into infrastructure-scale work.",
        reality_check="Electrical Engineering is a serious, respected branch with real industrial demand — but it is less socially hyped than computing. Students who chase only hype miss the fact that EE roles in power, energy, and control are often less competitive and more stable than crowded software markets.",
        choose_if="Choose EE if you like power systems, control, machines, energy infrastructure, and engineering that directly touches the physical world at scale.",
        avoid_if="Avoid EE if you dislike physics-heavy analytical work and only want trendy narratives with instant social validation.",
        what_you_study=[
            "Circuit analysis, electrical machines (motors, generators, transformers), and power electronics",
            "Power systems — generation, transmission, distribution, protection, and grid management",
            "Control systems — how feedback loops stabilize industrial processes and machines",
            "Signals, electromagnetic theory, and instrumentation fundamentals",
            "Power electronics and drives — converting and controlling electrical energy efficiently",
            "Electives in renewable energy, smart grids, electric vehicles, or high-voltage engineering",
        ],
        problems_and_work=[
            "Designing electrical distribution systems for buildings, factories, or industrial plants",
            "Working on power grid stability, load management, and fault protection",
            "Developing control systems for industrial automation, motors, and drives",
            "Testing and commissioning electrical equipment — transformers, switchgear, protection relays",
            "Working on renewable energy integration — solar, wind, battery storage systems",
            "Designing and validating EV charging infrastructure and power conversion systems",
        ],
        roles=[
            "Power Systems Engineer — working on grid design, load analysis, and power distribution",
            "Control Engineer — designing feedback and automation systems for industrial processes",
            "Electrical Design Engineer — creating electrical layouts and specifications for projects",
            "Instrumentation Engineer — working with sensors, measurement, and process control",
            "Renewable Energy Engineer — designing solar, wind, or storage systems",
            "Plant / Industrial Engineer — managing electrical systems in manufacturing facilities",
        ],
        tradeoffs=[
            "The theory is math-heavy and physics-intensive — if you do not like that, the branch feels punishing",
            "Many of the best roles are in specific industries (power, oil & gas, manufacturing) rather than generic tech",
            "Starting salaries may feel modest compared to software, but stability and growth in the right domains are strong",
            "You may need patience with career visibility — EE work is critical but rarely Instagram-worthy",
        ],
        good_fit_checklist=[
            "I like power systems, energy, or industrial engineering",
            "I am comfortable with physics-heavy analytical rigor",
            "I care about real infrastructure that actually keeps things running",
            "I want engineering depth over branch-name trendiness",
            "I find electrical machines, control loops, or energy systems genuinely interesting",
        ],
        misconceptions=[
            "\"Electrical is the same as Electronics.\" — They share foundations but diverge significantly. EE leans power and infrastructure. ECE leans devices and communication.",
            "\"EE is only for government jobs.\" — Private sector demand is huge in power, manufacturing, renewables, EVs, and industrial automation.",
            "\"The branch is boring.\" — If you think keeping an entire country's power grid stable is boring, you might not understand what interesting means at infrastructure scale.",
            "\"EE graduates cannot get into software.\" — Many do. But the real question is whether software is actually what you want, or just what everyone told you to want.",
        ],
        example_projects=[
            "Designing the electrical distribution system for a new hospital — load calculations, backup power, and safety systems",
            "Building a solar microgrid for a rural community with battery storage and smart load management",
            "Developing a PID control system that maintains temperature in an industrial furnace within ±2°C",
            "Testing and commissioning a 132kV substation and its protection relay coordination",
            "Designing the power electronics for an EV fast-charging station",
        ],
        similar_branches=["Electrical and Electronics Engineering", "Electronics and Communication Engineering", "Engineering Physics"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and circuit basics",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, complex analysis, linear algebra, transforms \u2014 math for circuit and system analysis",
                                        "tests": "Written exams with heavy transform and differential equation problems"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Electromagnetics, quantum physics, semiconductor basics \u2014 physics underlying electrical systems",
                                        "tests": "Theory exams plus lab experiments on electromagnetic phenomena"
                                },
                                {
                                        "name": "Basic Electrical Engineering",
                                        "teaches": "DC/AC circuits, Kirchhoff's laws, basic machines, power measurement \u2014 the starting point",
                                        "tests": "Circuit analysis problems; basic electrical measurement lab"
                                },
                                {
                                        "name": "Introduction to Programming",
                                        "teaches": "C/Python programming, logic, functions \u2014 coding for simulation and control applications later",
                                        "tests": "Lab coding exams; written exam on programming concepts"
                                },
                                {
                                        "name": "Engineering Drawing / Workshop",
                                        "teaches": "Technical drawing, electrical wiring practice, basic fabrication",
                                        "tests": "Drawing sheets and workshop practical assessment"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Core electrical \u2014 machines, circuits, fields, and signals",
                        "courses": [
                                {
                                        "name": "Circuit Theory",
                                        "teaches": "Network theorems, transient analysis, AC steady state, resonance \u2014 systematic circuit analysis",
                                        "tests": "Heavy numerical circuit problems; lab verification of network theorems"
                                },
                                {
                                        "name": "Electrical Machines I",
                                        "teaches": "DC machines, transformers \u2014 how motors, generators, and transformers work physically and electrically",
                                        "tests": "Machine testing lab (load tests, efficiency); written analysis problems"
                                },
                                {
                                        "name": "Electromagnetic Fields",
                                        "teaches": "Maxwell's equations, wave propagation, boundary conditions \u2014 the physics of electrical systems",
                                        "tests": "Derivation-heavy exams; field computation problems"
                                },
                                {
                                        "name": "Signals and Systems",
                                        "teaches": "Fourier and Laplace analysis, system response, convolution \u2014 mathematical signal framework",
                                        "tests": "Transform-heavy written exams; MATLAB signal analysis labs"
                                },
                                {
                                        "name": "Electrical Measurements",
                                        "teaches": "Instrument transformers, bridges, oscilloscopes, measurement uncertainty \u2014 precision measurement",
                                        "tests": "Measurement lab practicals; instrument handling assessment"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Power systems, control, and power electronics",
                        "courses": [
                                {
                                        "name": "Power Systems Analysis",
                                        "teaches": "Load flow, fault analysis, stability, economic dispatch \u2014 how the electrical grid works",
                                        "tests": "Power flow computation problems; simulation assignments using PowerWorld/ETAP"
                                },
                                {
                                        "name": "Control Systems",
                                        "teaches": "Transfer functions, stability criteria, root locus, Bode plots, state space \u2014 system control theory",
                                        "tests": "Stability analysis problems; control lab with servo motor and PID tuning"
                                },
                                {
                                        "name": "Power Electronics",
                                        "teaches": "Rectifiers, inverters, choppers, AC regulators \u2014 converting and controlling electrical power",
                                        "tests": "Power converter design problems; power electronics lab with thyristor circuits"
                                },
                                {
                                        "name": "Electrical Machines II",
                                        "teaches": "Induction motors, synchronous machines, special machines \u2014 advanced rotating machine behavior",
                                        "tests": "Machine testing lab (no-load, blocked rotor tests); performance analysis problems"
                                },
                                {
                                        "name": "Switchgear & Protection",
                                        "teaches": "Relay coordination, circuit breakers, fault protection \u2014 keeping power systems safe",
                                        "tests": "Protection scheme design problems; relay testing lab experiments"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Advanced power, renewables, and capstone",
                        "courses": [
                                {
                                        "name": "Renewable Energy Systems (elective)",
                                        "teaches": "Solar PV design, wind energy systems, energy storage, grid integration of renewables",
                                        "tests": "Solar/wind system design project; written exam on renewable energy technology"
                                },
                                {
                                        "name": "High Voltage Engineering (elective)",
                                        "teaches": "Insulation, breakdown mechanisms, testing techniques, lightning protection",
                                        "tests": "High voltage lab experiments; insulation design problems"
                                },
                                {
                                        "name": "Smart Grid Technology (elective)",
                                        "teaches": "Advanced metering, demand response, distributed generation, grid automation",
                                        "tests": "Case study analysis; simulation project on smart grid scenarios"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "Complete electrical engineering project: design, simulation, testing, and defense",
                                        "tests": "Working simulation or hardware demo, project report, viva voce"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Chemical Engineering",
        slug="chemical-engineering",
        family="process",
        overview="The engineering of industrial processes — designing, optimizing, and scaling systems that transform raw materials into useful products. Chemical engineers think in terms of mass balance, energy balance, reaction kinetics, and process economics.",
        who_this_fits="students who enjoy process thinking, industrial-scale systems, chemistry-linked engineering, and solving problems where scale changes everything",
        eli10="You learn how factories take raw materials and turn them into useful things — medicines, plastics, fuels, food products, fertilizers — safely, efficiently, and at massive scale. It is like cooking, but the kitchen is a factory and the recipe has thermodynamics.",
        school_connection="If you liked chemistry (especially physical chemistry, reactions, and energy) and enjoyed thinking about how processes work at scale rather than just in test tubes, Chemical Engineering takes that into industrial-grade problem solving.",
        reality_check="Chemical Engineering is NOT class-12 chemistry in a hard hat. It is fundamentally about process systems, transport phenomena, thermodynamics, and scale-up. Students who expect school chemistry get confused fast. Students who embrace the systems-thinking side find it incredibly rewarding.",
        choose_if="Choose Chemical Engineering if you like industrial systems, process optimization, and the challenge of making things work at scale — not just in a lab, but in a real plant.",
        avoid_if="Avoid it if the only reason you are choosing it is because you scored well in school chemistry, without checking whether you actually enjoy process and industrial thinking.",
        what_you_study=[
            "Thermodynamics and chemical reaction engineering — the energy and transformation fundamentals",
            "Transport phenomena — how mass, heat, and momentum move through industrial systems",
            "Process design and simulation — designing plants and optimizing their operation",
            "Separation processes — distillation, extraction, filtration, and how mixtures get divided into useful components",
            "Process control and instrumentation — how plants self-regulate and stay safe",
            "Electives in petroleum engineering, biochemical engineering, polymer science, or environmental engineering",
        ],
        problems_and_work=[
            "Designing chemical reactors, distillation columns, and heat exchangers for new production lines",
            "Optimizing plant operations to reduce energy consumption, waste, and production costs",
            "Scaling up a laboratory process to industrial production — where everything that worked small suddenly breaks",
            "Ensuring plant safety through hazard analysis, pressure relief design, and emergency planning",
            "Working on water treatment, emission control, and environmental compliance for industrial facilities",
            "Managing quality control and process troubleshooting in pharma, petrochemical, or food processing plants",
        ],
        roles=[
            "Process Engineer — designing and optimizing manufacturing processes",
            "Plant / Production Engineer — running and improving factory operations",
            "R&D Engineer — developing new products, formulations, or process technologies",
            "Quality / Regulatory Engineer — ensuring products meet safety and compliance standards",
            "Energy / Sustainability Engineer — working on efficiency, waste reduction, and green processes",
            "Petrochemical / Refinery Engineer — working in oil, gas, and chemical processing facilities",
        ],
        tradeoffs=[
            "Some of the best roles are plant-based and location-specific — chemical plants are not in every city",
            "The branch is great for students who like it, but confusing for those expecting generic office work",
            "Higher education (M.Tech, MS, or MBA) can significantly expand options beyond plant roles",
            "The process industry has safety stakes — mistakes can have serious consequences, so precision matters",
        ],
        good_fit_checklist=[
            "I like process thinking and understanding how large-scale systems work",
            "I do not mind industry-facing or plant-facing engineering work",
            "I am curious about how products get manufactured at scale — from raw materials to finished goods",
            "I want engineering that combines science, operations, and industrial reality",
            "I can handle the idea that some roles involve factories, shifts, or field exposure",
        ],
        misconceptions=[
            "\"Chemical Engineering is just chemistry.\" — It is really about engineering processes at scale. The chemistry is one input; the rest is thermodynamics, fluid mechanics, heat transfer, and economics.",
            "\"There are no jobs.\" — The process industry (pharma, FMCG, oil & gas, specialty chemicals) is massive. The jobs exist — they are just not all in Bangalore.",
            "\"You will be stuck in a factory forever.\" — Many chemical engineers move into consulting, management, R&D, or business roles after a few years of plant experience.",
            "\"It is not relevant to modern technology.\" — Battery manufacturing, semiconductor process engineering, and bioprocess design are all chemical engineering problems.",
        ],
        example_projects=[
            "Designing a distillation system to separate ethanol and water for a biofuel plant",
            "Running a HAZOP (Hazard and Operability) study for a new pharmaceutical production facility",
            "Optimizing a fertilizer plant's ammonia reactor to increase yield by 8% while reducing energy use",
            "Scaling up a lab-developed biodegradable plastic formulation to pilot-plant production",
            "Designing a wastewater treatment system for a textile factory to meet discharge standards",
        ],
        similar_branches=["Metallurgical and Materials Engineering", "Bio Technology", "Petroleum Engineering"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and process basics",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, ODEs, linear algebra \u2014 math for mass and energy balance calculations",
                                        "tests": "Written exams focused on applied problem solving"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Thermodynamics basics, fluid properties, heat \u2014 physics relevant to process engineering",
                                        "tests": "Theory exams and physics lab practicals"
                                },
                                {
                                        "name": "Engineering Chemistry",
                                        "teaches": "Chemical bonding, reaction kinetics, electrochemistry, polymers \u2014 chemistry foundations for ChemE",
                                        "tests": "Written exam plus detailed chemistry lab practical and reports"
                                },
                                {
                                        "name": "Introduction to Chemical Engineering",
                                        "teaches": "Mass balance, energy balance, unit operations overview \u2014 the language of the discipline",
                                        "tests": "Mass/energy balance calculation problems; introductory process flowsheet exercises"
                                },
                                {
                                        "name": "Engineering Drawing / Workshop",
                                        "teaches": "Technical drawing, pipe fitting, basic fabrication relevant to process plants",
                                        "tests": "Drawing assessment and workshop practical evaluation"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Core process engineering \u2014 thermo, fluids, and heat transfer",
                        "courses": [
                                {
                                        "name": "Chemical Engineering Thermodynamics",
                                        "teaches": "Laws of thermodynamics, phase equilibria, fugacity, activity coefficients \u2014 energy analysis for processes",
                                        "tests": "Thermodynamic cycle and equilibrium problems; heavy on numerical calculations"
                                },
                                {
                                        "name": "Fluid Mechanics for Chemical Engineers",
                                        "teaches": "Fluid statics, pipe flow, pumps, compressors, non-Newtonian fluids \u2014 moving materials through plants",
                                        "tests": "Pipe flow and pump sizing problems; fluid mechanics lab with flow measurement"
                                },
                                {
                                        "name": "Heat Transfer",
                                        "teaches": "Conduction, convection, radiation, heat exchanger design \u2014 thermal energy management in processes",
                                        "tests": "Heat exchanger design problems; lab experiments measuring heat transfer coefficients"
                                },
                                {
                                        "name": "Chemical Process Calculations",
                                        "teaches": "Material and energy balances on complex process flowsheets with recycle and bypass streams",
                                        "tests": "Multi-unit process balance problems; flowsheet analysis assignments"
                                },
                                {
                                        "name": "Organic / Inorganic Chemical Technology",
                                        "teaches": "Industrial manufacturing of acids, alkalis, fertilizers, petrochemicals \u2014 how chemicals get made",
                                        "tests": "Written exam on process descriptions; plant visit reports"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Reaction engineering, mass transfer, and process control",
                        "courses": [
                                {
                                        "name": "Chemical Reaction Engineering",
                                        "teaches": "Reactor design (CSTR, PFR, batch), kinetics, conversion, selectivity \u2014 the heart of chemical processing",
                                        "tests": "Reactor design and sizing problems; reaction kinetics lab experiments"
                                },
                                {
                                        "name": "Mass Transfer Operations",
                                        "teaches": "Distillation, absorption, extraction, drying, crystallization \u2014 separating mixtures at scale",
                                        "tests": "Column design problems; mass transfer lab (distillation, extraction experiments)"
                                },
                                {
                                        "name": "Process Dynamics and Control",
                                        "teaches": "Process modeling, feedback control, PID tuning, stability \u2014 keeping plants operating safely",
                                        "tests": "Control system design problems; process control lab with simulation"
                                },
                                {
                                        "name": "Transport Phenomena",
                                        "teaches": "Unified treatment of momentum, heat, and mass transfer \u2014 the theoretical backbone of ChemE",
                                        "tests": "Analytical and numerical problems; heavy on mathematical derivation"
                                },
                                {
                                        "name": "Process Equipment Design",
                                        "teaches": "Pressure vessel design, distillation column internals, storage tanks \u2014 designing real plant hardware",
                                        "tests": "Equipment design project with mechanical drawing; code-based sizing calculations"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Plant design, safety, and capstone",
                        "courses": [
                                {
                                        "name": "Process Plant Design & Economics",
                                        "teaches": "Process synthesis, optimization, cost estimation, profitability analysis \u2014 designing viable plants",
                                        "tests": "Complete plant design project with economic evaluation; group presentation"
                                },
                                {
                                        "name": "Process Safety & Hazard Analysis",
                                        "teaches": "HAZOP, fault trees, risk assessment, safety systems \u2014 preventing industrial disasters",
                                        "tests": "HAZOP case study analysis; safety audit report on a real or simulated process"
                                },
                                {
                                        "name": "Environmental Engineering (elective)",
                                        "teaches": "Wastewater treatment, air pollution control, waste management for chemical industries",
                                        "tests": "Treatment system design problems; environmental compliance case studies"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "End-to-end process design or research project: problem, design, simulation, and defense",
                                        "tests": "Process simulation demo, written report, viva with external examiner"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Metallurgical and Materials Engineering",
        slug="metallurgical-and-materials-engineering",
        family="materials",
        overview="The branch that studies what things are made of, why materials behave differently, and how choosing the right material transforms engineering outcomes. From steel bridges to silicon chips to titanium implants — materials decisions shape everything.",
        who_this_fits="students curious about metals, alloys, ceramics, material behavior, manufacturing science, and why things fail or survive under stress",
        eli10="You learn why some metals bend, some crack, some survive extreme heat, and why choosing the right material can make or break an entire engineering project. The next time a plane wing does not snap off mid-flight — materials engineers are part of why.",
        school_connection="If you liked chemistry (especially solid-state and bonding) or physics (especially properties of matter) and found yourself curious about why different materials behave so differently, this branch turns that curiosity into engineering expertise.",
        reality_check="This branch sounds narrow to outsiders, but materials thinking shows up in aerospace, automotive, electronics, energy, manufacturing, and biomedical engineering. It is often underestimated because the name sounds old-school, while the actual work is increasingly high-tech.",
        choose_if="Choose this branch if you enjoy applied science inside engineering, want to understand strength, durability, processing, and performance at a deep level, and do not need the trendiest brand name to feel confident.",
        avoid_if="Avoid it if you need instant brand recognition from your branch name and have zero interest in materials, industry, or manufacturing depth.",
        what_you_study=[
            "Physical metallurgy — phase diagrams, crystal structures, heat treatment, and how microstructure determines properties",
            "Mechanical metallurgy — how materials deform, fracture, fatigue, and fail under different loading conditions",
            "Extractive metallurgy — how metals are extracted and refined from ores (iron, aluminum, copper, etc.)",
            "Materials characterization — using SEM, XRD, and spectroscopy to study material structure and composition",
            "Corrosion science and surface engineering — why metals degrade and how to protect them",
            "Electives in ceramics, polymers, composites, biomaterials, or nanomaterials depending on college",
        ],
        problems_and_work=[
            "Selecting the right material for automotive or aerospace components that must balance weight, strength, and cost",
            "Investigating why a component failed in service and recommending design or material changes to prevent recurrence",
            "Designing heat treatment processes that give steel the right combination of hardness, toughness, and weldability",
            "Developing quality control procedures for steel mills, foundries, or manufacturing plants",
            "Working on advanced materials — composites for wind turbines, biocompatible alloys for implants, or semiconductor materials",
            "Consulting on corrosion protection systems for pipelines, marine structures, or chemical plants",
        ],
        roles=[
            "Materials Engineer — selecting, testing, and improving materials for products and processes",
            "Metallurgist — working in steel, aluminum, or metals production and processing",
            "Quality / Failure Analysis Engineer — investigating failures and ensuring product reliability",
            "R&D Engineer — developing new materials or processing techniques",
            "Process Engineer (metals) — optimizing casting, forging, heat treatment, or welding processes",
            "Corrosion Engineer — protecting infrastructure and equipment from degradation",
        ],
        tradeoffs=[
            "The branch name causes more hesitation than the actual career prospects deserve",
            "Some roles can be specialized and domain-specific compared with generic software careers",
            "Higher education (MS, PhD) can dramatically open up advanced R&D and materials science roles",
            "The best outcomes come from leaning into the domain rather than apologizing for the branch name",
        ],
        good_fit_checklist=[
            "I like understanding what products are made of and why specific materials are chosen",
            "I enjoy applied science more than superficial trend-following",
            "I can appreciate specialized industrial domains — steel, aerospace, automotive, energy",
            "I do not need mass-market prestige to feel confident in my career path",
            "I find failure analysis, testing, and material behavior genuinely fascinating",
        ],
        misconceptions=[
            "\"The branch is only about old-fashioned metalwork.\" — Modern materials engineering covers nanomaterials, biomaterials, semiconductor materials, and advanced composites.",
            "\"There are no jobs.\" — Steel companies, automotive OEMs, aerospace firms, and research labs actively hire materials/metallurgy graduates.",
            "\"You need a PhD to do anything useful.\" — Many impactful roles exist at the B.Tech level in production, quality, and process engineering. Higher degrees expand the ceiling, not the floor.",
            "\"It is irrelevant to modern technology.\" — Every semiconductor chip, every EV battery, every aircraft engine depends on materials engineering decisions.",
        ],
        example_projects=[
            "Investigating fatigue failure in a railway axle and recommending material and process changes",
            "Designing a heat treatment cycle for automotive gears to achieve the right hardness and toughness",
            "Characterizing a new aluminum alloy using SEM and tensile testing for lightweight vehicle applications",
            "Developing a corrosion-resistant coating for offshore oil platform structures",
            "Analyzing weld quality in pipeline construction using non-destructive testing methods",
        ],
        similar_branches=["Chemical Engineering", "Mechanical Engineering", "Engineering Physics"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and materials introduction",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, linear algebra, statistics \u2014 math for materials analysis and process calculations",
                                        "tests": "Written problem-solving exams"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Crystallography, X-ray diffraction basics, quantum mechanics \u2014 physics of solid materials",
                                        "tests": "Theory exams plus lab on crystal structure and diffraction"
                                },
                                {
                                        "name": "Engineering Chemistry",
                                        "teaches": "Electrochemistry, corrosion basics, thermochemistry \u2014 chemistry of metals and reactions",
                                        "tests": "Written exam and chemistry lab practicals"
                                },
                                {
                                        "name": "Introduction to Materials Science",
                                        "teaches": "Atomic bonding, crystal structures, defects, material classification \u2014 the branch orientation",
                                        "tests": "Written exam on structure-property basics; specimen identification lab"
                                },
                                {
                                        "name": "Engineering Drawing / Workshop",
                                        "teaches": "Technical drawing, foundry, welding, fitting \u2014 manufacturing process exposure",
                                        "tests": "Drawing sheets and workshop practical assessment"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Physical metallurgy \u2014 structure, phases, and properties",
                        "courses": [
                                {
                                        "name": "Physical Metallurgy",
                                        "teaches": "Phase diagrams, solidification, diffusion, nucleation and growth \u2014 how microstructure forms",
                                        "tests": "Phase diagram problems; metallography lab examining microstructures under microscope"
                                },
                                {
                                        "name": "Mineral Processing",
                                        "teaches": "Crushing, grinding, flotation, gravity separation \u2014 extracting valuable minerals from ore",
                                        "tests": "Mineral processing lab with separation experiments; flowsheet design problems"
                                },
                                {
                                        "name": "Iron and Steelmaking",
                                        "teaches": "Blast furnace, BOF, EAF, secondary refining \u2014 how iron ore becomes steel at industrial scale",
                                        "tests": "Process calculation problems; plant visit reports; steelmaking simulation"
                                },
                                {
                                        "name": "Thermodynamics of Materials",
                                        "teaches": "Free energy, equilibria, Ellingham diagrams, activity \u2014 predicting what reactions occur and when",
                                        "tests": "Thermodynamic calculation problems; Ellingham diagram analysis"
                                },
                                {
                                        "name": "Mechanical Behavior of Materials",
                                        "teaches": "Tensile, hardness, impact, fatigue, creep testing \u2014 quantifying how materials perform under stress",
                                        "tests": "Mechanical testing lab (UTM, hardness tester, impact machine); data analysis reports"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Processing, corrosion, and advanced characterization",
                        "courses": [
                                {
                                        "name": "Mechanical Metallurgy",
                                        "teaches": "Dislocations, strengthening mechanisms, fracture mechanics, fatigue \u2014 why materials fail",
                                        "tests": "Failure analysis problems; fractography lab examining fracture surfaces"
                                },
                                {
                                        "name": "Heat Treatment",
                                        "teaches": "Annealing, quenching, tempering, case hardening, TTT/CCT diagrams \u2014 controlling properties through thermal processing",
                                        "tests": "Heat treatment lab (heating, quenching, testing hardness); TTT diagram analysis"
                                },
                                {
                                        "name": "Corrosion Engineering",
                                        "teaches": "Electrochemical corrosion, types of corrosion, prevention methods, coatings, cathodic protection",
                                        "tests": "Corrosion testing lab; protection system design problems; case studies"
                                },
                                {
                                        "name": "Non-Ferrous Extractive Metallurgy",
                                        "teaches": "Extraction of aluminum, copper, zinc, titanium \u2014 hydrometallurgy and pyrometallurgy processes",
                                        "tests": "Process flowsheet and calculation problems; comparison of extraction routes"
                                },
                                {
                                        "name": "Materials Characterization",
                                        "teaches": "SEM, XRD, TEM, spectroscopy techniques \u2014 tools for studying material structure at micro/nano scale",
                                        "tests": "Characterization lab using actual instruments; data interpretation assignments"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Advanced materials, applications, and capstone",
                        "courses": [
                                {
                                        "name": "Advanced Materials (elective)",
                                        "teaches": "Composites, nanomaterials, biomaterials, smart materials \u2014 frontier material systems",
                                        "tests": "Literature review project; written exam on advanced material properties"
                                },
                                {
                                        "name": "Welding Metallurgy (elective)",
                                        "teaches": "Weld microstructure, heat affected zones, weld defects, qualification \u2014 metallurgy of joining",
                                        "tests": "Weld testing lab; defect analysis case studies"
                                },
                                {
                                        "name": "Failure Analysis (elective)",
                                        "teaches": "Systematic failure investigation: fracture, fatigue, corrosion, wear \u2014 determining root causes",
                                        "tests": "Failure case study project with full investigation report"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "Complete materials/metallurgy research or design project: experimentation, characterization, analysis",
                                        "tests": "Lab results presentation, written thesis, viva with external examiner"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Electrical and Electronics Engineering",
        slug="electrical-and-electronics-engineering",
        family="electronics",
        overview="A blend of electrical power systems and electronics, sitting between the infrastructure scale of EE and the device-level depth of ECE. Think of it as the branch that refuses to pick a side — and that can be a feature, not a bug.",
        who_this_fits="students who want overlap between electrical infrastructure and electronic systems rather than committing fully to one narrow direction",
        eli10="You learn both the bigger electrical world (power, motors, grids) and the smaller electronics world (circuits, devices, chips), so you can work on systems that need both — like factory automation, control panels, or smart grid equipment.",
        school_connection="If you liked physics (especially electricity and circuits) and found both the large-scale (power plants) and small-scale (electronic devices) sides interesting, EEE lets you keep both without forcing a premature choice.",
        reality_check="EEE can be genuinely versatile, but it rewards active self-direction. If you drift through the curriculum without building depth in any specific area, the branch feels vague. If you shape it deliberately through projects and electives, it becomes flexible in a useful way.",
        choose_if="Choose EEE if you want a middle ground between power/electrical infrastructure and electronics/embedded systems, and you are willing to actively shape your specialization.",
        avoid_if="Avoid EEE if you need a hyper-specific branch identity from day one and do not want the responsibility of choosing your own depth.",
        what_you_study=[
            "Electrical circuits, machines (motors, transformers), and power system fundamentals",
            "Analog and digital electronics, microprocessors, and basic semiconductor physics",
            "Control systems and instrumentation — how systems regulate themselves",
            "Power electronics — converting and controlling electrical energy for industrial and consumer applications",
            "Basics of communication systems and signal processing",
            "Electives that let you lean toward either the power side or the electronics side depending on interest",
        ],
        problems_and_work=[
            "Designing control and automation systems for factories, production lines, or building management",
            "Working on industrial electronics — drives, power supplies, UPS systems, and inverters",
            "Developing and testing electronic subsystems for automotive, appliance, or industrial products",
            "Managing electrical and electronic systems in manufacturing plants or infrastructure projects",
            "Working on smart grid technology, renewable energy integration, or EV power systems",
            "Bridging the gap between electrical infrastructure teams and electronic product development teams",
        ],
        roles=[
            "Control and Automation Engineer — designing systems that run factories and processes automatically",
            "Power Electronics Engineer — working on drives, converters, and energy management systems",
            "Industrial Electronics Engineer — maintaining and improving electronic systems in production environments",
            "Systems Engineer — integrating electrical and electronic subsystems in complex products",
            "Test / Validation Engineer — ensuring electrical and electronic products meet specifications",
            "Software Engineer — many EEE graduates transition into software with strong systems understanding",
        ],
        tradeoffs=[
            "The overlap with EE and ECE confuses students — you need to understand what your specific college's curriculum emphasizes",
            "Outcomes depend heavily on what electives, projects, and internships you choose — passive students get vague results",
            "The branch can feel broad in a good way (flexibility) or bad way (no clear identity) depending on how you handle it",
            "Some employers may not clearly distinguish between EE, ECE, and EEE when hiring — which can work for or against you",
        ],
        good_fit_checklist=[
            "I want both electrical and electronics exposure without being forced to pick one too early",
            "I am okay with actively shaping my own focus through projects and electives",
            "I like real-world systems that touch the physical world — not purely abstract or digital work",
            "I am willing to build depth in a specific area rather than staying surface-level across everything",
            "I do not need a one-word branch identity to feel secure",
        ],
        misconceptions=[
            "\"EEE is just a diluted version of EE or ECE.\" — It is a blend, not a dilution. The value depends on how you use the breadth.",
            "\"Employers don't know what EEE is.\" — In industries like manufacturing, power, and automation, the EEE skillset is well understood and valued.",
            "\"You cannot specialize with an EEE degree.\" — You absolutely can — through electives, projects, internships, and M.Tech if needed.",
            "\"It is a safe middle-ground choice.\" — It is only safe if you actively direct it. Drifting through EEE without building any depth is riskier than committing to a clearer branch.",
        ],
        example_projects=[
            "Building a PLC-based automation system for a packaging line in a food processing plant",
            "Designing a solar inverter that converts DC from solar panels into AC for household use",
            "Developing a motor drive system that precisely controls speed and torque for an industrial robot",
            "Creating a smart energy monitoring system that tracks real-time power consumption in a building",
            "Testing and debugging an electronic control unit (ECU) for an automotive braking system",
        ],
        similar_branches=["Electrical Engineering", "Electronics and Communication Engineering", "Instrumentation Engineering"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and circuit basics",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, transforms, complex analysis \u2014 math shared with EE and ECE",
                                        "tests": "Written exams with transform and circuit math problems"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Electromagnetics, semiconductor physics, optics \u2014 physics for electrical and electronic systems",
                                        "tests": "Theory exam plus lab experiments"
                                },
                                {
                                        "name": "Basic Electrical & Electronics",
                                        "teaches": "DC/AC circuits, diodes, transistors, basic digital logic \u2014 dual foundation",
                                        "tests": "Circuit analysis problems and introductory electronics lab"
                                },
                                {
                                        "name": "Introduction to Programming",
                                        "teaches": "C programming, logic, functions \u2014 coding for embedded and control applications",
                                        "tests": "Lab coding exams; written exam on programming concepts"
                                },
                                {
                                        "name": "Engineering Drawing / Workshop",
                                        "teaches": "Technical drawing, electrical wiring, PCB basics, soldering",
                                        "tests": "Drawing sheets and workshop practical assessment"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Dual foundation \u2014 electrical machines and electronic circuits",
                        "courses": [
                                {
                                        "name": "Circuit Theory",
                                        "teaches": "Network analysis, transients, AC steady state, two-port networks \u2014 shared EE/ECE foundation",
                                        "tests": "Circuit analysis problems; lab verification experiments"
                                },
                                {
                                        "name": "Electrical Machines",
                                        "teaches": "DC machines, transformers, induction motors \u2014 how electromechanical energy conversion works",
                                        "tests": "Machine testing lab; performance analysis calculations"
                                },
                                {
                                        "name": "Electronic Devices & Circuits",
                                        "teaches": "Semiconductor devices, amplifiers, biasing, frequency response \u2014 analog electronics foundation",
                                        "tests": "Circuit design problems; electronics lab building amplifier circuits"
                                },
                                {
                                        "name": "Digital Electronics",
                                        "teaches": "Logic gates, combinational/sequential circuits, memory, basic microprocessor concepts",
                                        "tests": "Digital logic design problems; digital lab on trainer kits"
                                },
                                {
                                        "name": "Signals and Systems",
                                        "teaches": "Fourier and Laplace transforms, system response, convolution \u2014 signal analysis framework",
                                        "tests": "Transform-heavy written exams; MATLAB signal processing labs"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Power electronics, control, and embedded systems",
                        "courses": [
                                {
                                        "name": "Power Electronics",
                                        "teaches": "Rectifiers, inverters, choppers, PWM \u2014 converting and controlling electrical power efficiently",
                                        "tests": "Converter design problems; power electronics lab with thyristor/MOSFET circuits"
                                },
                                {
                                        "name": "Control Systems",
                                        "teaches": "Transfer functions, stability, root locus, Bode plots, PID controllers \u2014 feedback system design",
                                        "tests": "Stability analysis problems; control lab with servo motor experiments"
                                },
                                {
                                        "name": "Microprocessors & Embedded Systems",
                                        "teaches": "Processor architecture, assembly programming, interfacing, real-time system concepts",
                                        "tests": "Embedded programming lab; interfacing project with sensors and actuators"
                                },
                                {
                                        "name": "Power Systems Basics",
                                        "teaches": "Generation, transmission, distribution, load flow, fault analysis \u2014 power grid fundamentals",
                                        "tests": "Power system calculation problems; simulation assignments"
                                },
                                {
                                        "name": "Communication Systems (overview)",
                                        "teaches": "Modulation, demodulation, noise, basic wireless concepts \u2014 introductory communication theory",
                                        "tests": "Modulation analysis problems; communication lab experiments"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Advanced applications and capstone",
                        "courses": [
                                {
                                        "name": "Drives and Industrial Automation (elective)",
                                        "teaches": "Motor drives, PLCs, SCADA, industrial control systems \u2014 factory automation",
                                        "tests": "PLC programming lab; drive simulation project"
                                },
                                {
                                        "name": "Renewable Energy Systems (elective)",
                                        "teaches": "Solar, wind, energy storage, grid integration \u2014 clean energy technology",
                                        "tests": "Renewable system design project; technology comparison analysis"
                                },
                                {
                                        "name": "Instrumentation & Sensors (elective)",
                                        "teaches": "Transducers, signal conditioning, measurement systems, data acquisition",
                                        "tests": "Sensor interfacing lab; measurement system design assignment"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "Integrated EEE project spanning electrical and electronic domains: design, build, test",
                                        "tests": "Working demo, written report, viva with external examiner"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Information Technology",
        slug="information-technology",
        family="computing",
        overview="A software-focused branch with strong overlap with CSE, often leaning more toward applications, databases, networking, web systems, and enterprise computing. In many colleges, the practical difference from CSE is smaller than the internet drama suggests.",
        who_this_fits="students who want software careers and care more about actual work fit than prestige label debates between CSE and IT",
        eli10="You learn how to build and manage the software systems that run businesses — apps, websites, databases, and the digital tools people use every day. If CSE is about 'how computers work,' IT is often more about 'how to make computers useful for people and organizations.'",
        school_connection="If you liked mathematics, logic, and computers, and found yourself more interested in building useful things (apps, websites, tools) than in pure theory — IT gives you a strong practical computing foundation.",
        reality_check="The CSE-vs-IT debate consumes more student anxiety than it deserves. In practice, the gap between them is often smaller than the gap between a good college and a mediocre one. The branch label matters less than your projects, internships, and ability to actually write solid code.",
        choose_if="Choose IT if you want practical software roles and are confident enough to not waste four years feeling insecure about a branch name.",
        avoid_if="Avoid IT if you are going to spend the entire degree comparing yourself to CSE students instead of building skill — that is a self-own of legendary proportions.",
        what_you_study=[
            "Programming, data structures, algorithms, and object-oriented design — the same core as CSE in most colleges",
            "Databases, SQL, data management, and information systems — how data gets stored, queried, and used",
            "Computer networks, web technologies, and distributed systems — how internet-scale software works",
            "Software engineering and development methodologies — how real teams build and ship software",
            "Cybersecurity, cloud computing, and system administration fundamentals",
            "Electives in web development, data science, DevOps, or enterprise systems depending on college",
        ],
        problems_and_work=[
            "Building web applications, mobile backends, REST APIs, and database-driven products",
            "Working on enterprise software — CRMs, ERPs, internal tools, and business automation",
            "Managing databases, optimizing queries, and designing data models for applications",
            "Setting up cloud infrastructure, CI/CD pipelines, and deployment automation",
            "Working on cybersecurity — protecting applications and systems from attacks and data breaches",
            "Building internal tools that help non-engineering teams work more efficiently",
        ],
        roles=[
            "Software Engineer — the same broad role that CSE graduates target",
            "Web / Backend Engineer — building the server-side logic and APIs that power products",
            "Database / Data Engineer — managing data infrastructure and pipelines",
            "DevOps / Cloud Engineer — automating deployment, scaling, and infrastructure management",
            "QA / Test Automation Engineer — ensuring software quality through systematic testing",
            "IT Consultant / Systems Analyst — helping organizations use technology more effectively",
        ],
        tradeoffs=[
            "Some students create unnecessary insecurity about the IT label — this is wasted energy, not a real career obstacle",
            "In a few elite institutions, CSE may have a marginally different curriculum — but in most colleges, the overlap is 80–90%",
            "The branch still demands real coding skill — there is no shortcut or free pass just because the name sounds more 'applied'",
            "Your actual outcomes depend on your code, your projects, and your interviews — not on whether your degree says CSE or IT",
        ],
        good_fit_checklist=[
            "I want software engineering roles and I am comfortable with coding-heavy learning",
            "I care more about the actual work I will do than semantic prestige debates on Quora",
            "I want broad practical computing options without the most competitive branch-cutoff pressure",
            "I am confident enough to define my worth through skill, not through a label",
            "I find building useful software more motivating than academic theory for its own sake",
        ],
        misconceptions=[
            "\"IT is inferior to CSE.\" — In most colleges, the curriculum overlap is huge and placement outcomes are nearly identical. The inferiority is manufactured anxiety, not engineering reality.",
            "\"IT graduates cannot get into top tech companies.\" — Google, Microsoft, Amazon, and others hire based on skill, not branch name. Your DSA and system design ability matters infinitely more.",
            "\"IT is just 'managing computers.'\" — Modern IT programs teach the same programming, algorithms, and system design that CSE does. The 'helpdesk' stereotype is decades out of date.",
            "\"You should always pick CSE over IT.\" — If the CSE cutoff forces you into a worse college, while IT gets you into a better one — IT at the better college often wins.",
        ],
        example_projects=[
            "Building a full-stack e-commerce application with user authentication, product search, and payment integration",
            "Designing a database schema and API backend for a food delivery startup",
            "Setting up a Kubernetes-based deployment pipeline that auto-scales based on traffic",
            "Creating a real-time chat application using WebSockets and a message queue",
            "Building a dashboard that aggregates data from multiple APIs and presents business metrics visually",
        ],
        similar_branches=["Computer Science and Engineering", "Mathematics and Computing", "Electronics and Communication Engineering"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and first programming",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, linear algebra, probability \u2014 math foundations for computing and data",
                                        "tests": "Written exams with problem-solving emphasis"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Mechanics, waves, optics, semiconductor basics \u2014 general science foundation",
                                        "tests": "Theory exam plus physics lab practicals"
                                },
                                {
                                        "name": "Introduction to Programming",
                                        "teaches": "Variables, control flow, functions, arrays, basic problem solving in C or Python",
                                        "tests": "Lab exams writing and running code under time constraints; written logic exam"
                                },
                                {
                                        "name": "Digital Logic",
                                        "teaches": "Boolean algebra, gates, flip-flops, basic processor concepts \u2014 how hardware computes",
                                        "tests": "Logic design problems; digital lab experiments on trainer kits"
                                },
                                {
                                        "name": "Engineering Drawing / Workshop",
                                        "teaches": "Technical drawing, basic fabrication, wiring \u2014 general engineering skills",
                                        "tests": "Drawing sheets and workshop practical evaluation"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Core computing \u2014 data structures, databases, and OOP",
                        "courses": [
                                {
                                        "name": "Data Structures & Algorithms",
                                        "teaches": "Arrays, linked lists, trees, graphs, sorting, searching, complexity analysis \u2014 the coding core",
                                        "tests": "Coding assignments and lab exams; written exam on algorithm analysis"
                                },
                                {
                                        "name": "Discrete Mathematics",
                                        "teaches": "Sets, logic, graph theory, combinatorics \u2014 formal mathematical reasoning for CS/IT",
                                        "tests": "Proof-based written exam; problem sets on discrete structures"
                                },
                                {
                                        "name": "Object-Oriented Programming",
                                        "teaches": "Classes, inheritance, polymorphism, design patterns \u2014 writing modular, maintainable code",
                                        "tests": "Coding projects; lab exams building OOP systems; written design principles exam"
                                },
                                {
                                        "name": "Database Management Systems",
                                        "teaches": "SQL, relational design, normalization, transactions, indexing \u2014 data storage and retrieval",
                                        "tests": "SQL lab exams; database design projects; written normalization theory exam"
                                },
                                {
                                        "name": "Computer Organization",
                                        "teaches": "CPU architecture, memory hierarchy, instruction execution \u2014 how hardware runs your code",
                                        "tests": "Written exam on architecture concepts; assembly programming assignments"
                                },
                                {
                                        "name": "Web Technologies",
                                        "teaches": "HTML, CSS, JavaScript, server-side basics \u2014 building web applications from scratch",
                                        "tests": "Web development project; lab exam building a functioning web page"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Systems, networks, security, and software engineering",
                        "courses": [
                                {
                                        "name": "Operating Systems",
                                        "teaches": "Process management, memory, file systems, concurrency \u2014 how software runs on hardware",
                                        "tests": "Written exam; coding assignments implementing OS concepts (scheduling, sync)"
                                },
                                {
                                        "name": "Computer Networks",
                                        "teaches": "TCP/IP, routing, HTTP, sockets, network security basics \u2014 how the internet works",
                                        "tests": "Network programming lab; packet analysis assignments; protocol-heavy written exam"
                                },
                                {
                                        "name": "Software Engineering",
                                        "teaches": "SDLC, requirements, testing, agile, CI/CD \u2014 how teams build and deliver software",
                                        "tests": "Group project building a real application; written exam on methodologies"
                                },
                                {
                                        "name": "Information Security",
                                        "teaches": "Cryptography, authentication, network security, ethical hacking, security policies",
                                        "tests": "Security analysis lab; penetration testing exercise; written crypto exam"
                                },
                                {
                                        "name": "Algorithm Design",
                                        "teaches": "Advanced algorithm techniques: DP, greedy, graph algorithms, complexity classes",
                                        "tests": "Algorithm design problems; competitive programming-style lab exams"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Cloud, data, and capstone",
                        "courses": [
                                {
                                        "name": "Cloud Computing (elective)",
                                        "teaches": "Virtualization, containers, AWS/Azure basics, microservices, serverless architecture",
                                        "tests": "Cloud deployment project; architecture design assignment"
                                },
                                {
                                        "name": "Data Mining & Analytics (elective)",
                                        "teaches": "Classification, clustering, association rules, text mining \u2014 extracting patterns from data",
                                        "tests": "Data analysis project with real dataset; written exam on algorithms"
                                },
                                {
                                        "name": "DevOps & Automation (elective)",
                                        "teaches": "CI/CD pipelines, Docker, Kubernetes, infrastructure as code, monitoring",
                                        "tests": "Pipeline setup project; automated deployment demo"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "End-to-end software project: requirements, design, implementation, testing, deployment",
                                        "tests": "Working application demo, written report, viva voce"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Bio Technology",
        slug="bio-technology",
        family="bio",
        overview="A biology-plus-engineering branch combining life sciences, bioprocess engineering, genetic techniques, and applied biological systems. For students who want to work at the intersection of biology and technology — not just study biology in a textbook.",
        who_this_fits="students who genuinely like biology and want technical, applied, research-oriented, or industry-linked career paths in life sciences",
        eli10="You use engineering ideas to work with living systems — cells, DNA, biological processes, and biotech tools that help create medicines, improve crops, make biofuels, and develop diagnostic tests. Imagine being the engineer inside a biology lab.",
        school_connection="If you liked biology (especially genetics, cell biology, and biochemistry) and found yourself more interested in applications and experiments than just memorizing diagrams, Biotech takes that into engineering territory.",
        reality_check="Biotech can be extremely rewarding for the right student, but it is rarely the branch to choose casually. If you do not actually like biology, laboratory science, or the possibility of higher studies amplifying your career — you will find the path frustrating and confusing.",
        choose_if="Choose Biotech if you genuinely enjoy biology and are open to labs, scientific research, biotech industry roles, and possibly higher-study-amplified career trajectories.",
        avoid_if="Avoid it if you only want the safest mainstream placement narrative and have no real interest in biological systems, lab work, or research-intensive careers.",
        what_you_study=[
            "Molecular biology, genetics, microbiology, and biochemistry — the core biological foundations",
            "Bioprocess engineering — how biological processes get scaled up for industrial production (fermentation, bioreactors)",
            "Genetic engineering and recombinant DNA technology — how genes get modified and expressed",
            "Immunology and bioinformatics — biological defense systems and computational biology tools",
            "Downstream processing — how biological products get purified and prepared for use",
            "Electives in pharmaceutical biotechnology, environmental biotech, food technology, or computational biology",
        ],
        problems_and_work=[
            "Developing and optimizing bioprocesses for manufacturing vaccines, antibodies, or enzymes at scale",
            "Working in quality control and regulatory affairs for pharmaceutical or biotech companies",
            "Conducting research on genetic modification, drug development, or diagnostic tool design",
            "Designing and running fermentation, cell culture, and purification processes in biotech facilities",
            "Analyzing biological data using bioinformatics tools and computational methods",
            "Supporting clinical trials, patent documentation, or technology transfer in biotech startups or pharma companies",
        ],
        roles=[
            "Bioprocess Engineer — designing and running biological manufacturing processes",
            "R&D Scientist / Research Associate — conducting experiments in biotech or pharma labs",
            "Quality Control / Quality Assurance — ensuring biotech products meet safety and regulatory standards",
            "Bioinformatics Analyst — using computational tools to analyze biological data",
            "Regulatory Affairs Specialist — managing product approvals and compliance documentation",
            "Academic Researcher (post higher studies) — working on cutting-edge biology and biotech problems",
        ],
        tradeoffs=[
            "Higher studies (M.Tech, MS, PhD) often matter significantly more here than in mainstream engineering branches",
            "Career paths can feel less obvious than plug-and-play software trajectories — you need to be intentional",
            "The best opportunities often require specialization, publications, or specific industry exposure",
            "Lab-based work can be slower-paced and more meticulous than students used to coding-speed feedback loops expect",
        ],
        good_fit_checklist=[
            "I actually enjoy biology — not just tolerate it, but find it genuinely interesting",
            "I am open to working in laboratories, research environments, or biotech industry settings",
            "I am comfortable with the possibility that higher studies may be important for my career growth",
            "I want science-heavy engineering rather than generic placement-focused programs",
            "I find the idea of working with living systems — cells, DNA, proteins — more exciting than intimidating",
        ],
        misconceptions=[
            "\"Biotech has no jobs.\" — The Indian biotech industry is growing rapidly, and global pharma/biotech companies actively hire. The jobs are there, but they require more intentional career planning.",
            "\"You will be stuck in a lab forever.\" — Many biotech graduates move into management, regulatory affairs, consulting, sales, or entrepreneurship. The lab is one starting path, not the only path.",
            "\"You need a PhD to do anything.\" — B.Tech graduates can work in bioprocess, QC/QA, and industry roles. Higher degrees expand research and leadership options, but are not mandatory for all paths.",
            "\"Biotech is just biology — not real engineering.\" — Bioprocess scale-up, fermentation engineering, and biomanufacturing involve serious engineering thinking. The 'just biology' perception is outdated.",
        ],
        example_projects=[
            "Optimizing a bacterial fermentation process to increase recombinant protein yield by 40%",
            "Designing a PCR-based diagnostic kit for rapid detection of a specific pathogen",
            "Running a bioinformatics analysis to identify potential drug targets in a disease pathway",
            "Scaling up a monoclonal antibody production process from lab flask to 500L bioreactor",
            "Developing a quality control protocol for testing batch-to-batch consistency in a vaccine manufacturing plant",
        ],
        similar_branches=["Biomedical Engineering", "Chemical Engineering", "Engineering Physics"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 math, science, and biology basics",
                        "courses": [
                                {
                                        "name": "Engineering Mathematics I & II",
                                        "teaches": "Calculus, statistics, linear algebra \u2014 math for bioprocess calculations and data analysis",
                                        "tests": "Written problem-solving exams"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Biophysics concepts, optics, spectroscopy basics \u2014 physics relevant to biological instrumentation",
                                        "tests": "Theory exam plus lab experiments"
                                },
                                {
                                        "name": "Engineering Chemistry",
                                        "teaches": "Organic chemistry, biochemistry basics, thermochemistry \u2014 chemical foundations for biotechnology",
                                        "tests": "Written exam plus chemistry lab focused on organic/biochem experiments"
                                },
                                {
                                        "name": "Biology for Engineers",
                                        "teaches": "Cell biology, genetics basics, microbiology introduction, evolution \u2014 the biological foundations",
                                        "tests": "Written exam on cell biology and genetics; biology lab with microscopy"
                                },
                                {
                                        "name": "Introduction to Biotechnology",
                                        "teaches": "Branch overview: medical, agricultural, industrial, environmental biotech applications",
                                        "tests": "Introductory written exam; seminar presentations on biotech applications"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Core biology \u2014 biochemistry, microbiology, and genetics",
                        "courses": [
                                {
                                        "name": "Biochemistry",
                                        "teaches": "Proteins, enzymes, metabolism, bioenergetics \u2014 the molecular machinery of living systems",
                                        "tests": "Written exam on metabolic pathways; biochemistry lab (enzyme assays, chromatography)"
                                },
                                {
                                        "name": "Microbiology",
                                        "teaches": "Bacteria, viruses, fungi, sterilization, culture techniques \u2014 working with microorganisms",
                                        "tests": "Microbiology lab (staining, culturing, identification); written exam on microbial biology"
                                },
                                {
                                        "name": "Cell Biology & Molecular Biology",
                                        "teaches": "Cell structure, gene expression, DNA replication, transcription, translation \u2014 the central dogma",
                                        "tests": "Written exam on molecular mechanisms; lab techniques (gel electrophoresis, PCR basics)"
                                },
                                {
                                        "name": "Bioprocess Engineering Fundamentals",
                                        "teaches": "Mass and energy balances for biological systems, reactor basics, sterilization engineering",
                                        "tests": "Bioprocess calculation problems; introduction to bioreactor lab"
                                },
                                {
                                        "name": "Genetics",
                                        "teaches": "Mendelian genetics, population genetics, gene mapping, chromosomal analysis",
                                        "tests": "Genetics problem sets; lab exercises in Drosophila genetics or computational genomics"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Applied biotech \u2014 genetic engineering, bioinformatics, and downstream processing",
                        "courses": [
                                {
                                        "name": "Genetic Engineering",
                                        "teaches": "Restriction enzymes, cloning, vectors, PCR, gene expression systems \u2014 manipulating DNA",
                                        "tests": "Cloning strategy design problems; molecular biology lab (restriction digestion, transformation)"
                                },
                                {
                                        "name": "Immunology",
                                        "teaches": "Immune system, antibodies, vaccines, diagnostic immunology \u2014 biological defense systems",
                                        "tests": "Written exam on immune mechanisms; immunology lab (ELISA, Western blot basics)"
                                },
                                {
                                        "name": "Bioinformatics",
                                        "teaches": "Sequence alignment, database searching, phylogenetics, structural prediction \u2014 computational biology",
                                        "tests": "Bioinformatics tool-based assignments (BLAST, multiple alignment); data analysis projects"
                                },
                                {
                                        "name": "Downstream Processing",
                                        "teaches": "Cell disruption, filtration, chromatography, drying \u2014 purifying biological products at scale",
                                        "tests": "Downstream processing lab; purification protocol design assignments"
                                },
                                {
                                        "name": "Biostatistics & Experimental Design",
                                        "teaches": "Hypothesis testing, ANOVA, regression, experimental planning \u2014 rigorous data analysis for biology",
                                        "tests": "Statistical analysis assignments using R or Excel; experimental design case studies"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Specialized biotech applications and capstone",
                        "courses": [
                                {
                                        "name": "Pharmaceutical Biotechnology (elective)",
                                        "teaches": "Drug development, biopharmaceuticals, clinical trials, regulatory science \u2014 medicines from biotech",
                                        "tests": "Drug development case study; regulatory pathway analysis assignment"
                                },
                                {
                                        "name": "Environmental Biotechnology (elective)",
                                        "teaches": "Bioremediation, waste treatment using microorganisms, biosensors for environmental monitoring",
                                        "tests": "Bioremediation project design; environmental microbiology lab"
                                },
                                {
                                        "name": "Industrial Biotechnology (elective)",
                                        "teaches": "Fermentation technology, enzyme technology, biofuels, food biotech \u2014 biotech at production scale",
                                        "tests": "Fermentation optimization project; industrial process case study analysis"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "Complete biotech research project: hypothesis, experimental design, lab work, analysis, defense",
                                        "tests": "Lab results presentation, written thesis, viva with external examiner"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Mathematics and Computing",
        slug="mathematics-and-computing",
        family="computing",
        overview="A quantitatively intense branch that fuses abstract mathematics with computing, algorithms, modeling, and analytical problem solving. This is not 'CSE with extra math' — it is a fundamentally different intellectual flavor where mathematical depth is the core identity.",
        who_this_fits="students who enjoy abstract math, algorithms, and analytical computing more than generic software hype — and want the quantitative depth to show in their work",
        eli10="It is like taking the math-heavy brain of computing and using it to solve harder problems — the kind where a regular programmer gets stuck but someone who really understands probability, optimization, and algorithms can see through the complexity.",
        school_connection="If you loved mathematics — not just scoring in it, but actually enjoying proofs, patterns, and abstract reasoning — and also liked coding, this branch is where those two interests stop competing and start collaborating.",
        reality_check="Mathematics and Computing sounds glamorous because it overlaps with quantitative roles that pay well. But the math is not decorative — it is foundational and relentless. Students who choose this for the status and not the abstraction can suffer spectacularly by the third semester.",
        choose_if="Choose this branch if you truly like mathematics and want computing with more analytical depth, quantitative reasoning, and intellectual challenge than the usual software narrative.",
        avoid_if="Avoid it if you dislike abstract reasoning and only want software because it seems lucrative — this branch will make you do hard math before you write any code.",
        what_you_study=[
            "Discrete mathematics, real analysis, linear algebra, and probability theory — the formal mathematical foundations",
            "Algorithms, data structures, and computational complexity — with more mathematical rigor than typical CS courses",
            "Optimization, numerical methods, and mathematical modeling — turning real problems into solvable mathematical structures",
            "Programming and software engineering — similar practical computing skills as CSE but with a quantitative spine",
            "Statistics and stochastic processes — the math behind data science, ML, and quantitative finance",
            "Electives in cryptography, machine learning theory, operations research, or mathematical finance",
        ],
        problems_and_work=[
            "Building algorithm-heavy software where mathematical insight gives you an edge over brute-force engineering",
            "Working on optimization problems in logistics, pricing, scheduling, or resource allocation",
            "Developing machine learning models with deeper understanding of why methods work, not just how to call libraries",
            "Solving quantitative problems in finance, trading systems, or risk modeling",
            "Creating cryptographic systems, security protocols, or privacy-preserving algorithms",
            "Conducting research or advanced engineering work where mathematical depth is a genuine requirement, not a resume decoration",
        ],
        roles=[
            "Software Engineer — with stronger algorithmic and mathematical foundations",
            "ML / Data Scientist — with deeper understanding of the math behind models",
            "Quantitative Analyst / Engineer — working in trading, finance, or analytics",
            "Research Engineer — in companies or labs working on hard computational problems",
            "Algorithm Engineer — building core algorithmic components of products (search, recommendations, matching)",
            "Cryptographer / Security Engineer — designing systems that depend on mathematical guarantees",
        ],
        tradeoffs=[
            "The math intensity is real and relentless — this is not a branch where you can coast through theory exams",
            "Students who choose it for prestige and then discover abstraction is not their friend face a genuinely painful experience",
            "The branch can be excellent for quantitative careers but may feel unnecessarily theoretical if you just want to build web apps",
            "You may need to explain your branch to people who have never heard of it — which is fine if you are secure in your choice",
        ],
        good_fit_checklist=[
            "I truly like math — not just scoring in math exams, but enjoying the reasoning",
            "I am comfortable with abstraction, proofs, and formal arguments",
            "I want computing with more quantitative depth than the typical software storyline",
            "I can trade some career-narrative simplicity for stronger intellectual fit",
            "I find solving hard mathematical problems genuinely satisfying, not just impressive-sounding",
        ],
        misconceptions=[
            "\"It is basically CSE with one extra math course.\" — The math is woven through everything, not sprinkled on top. The intellectual flavor is genuinely different.",
            "\"Only IIT students can do this branch.\" — The branch exists at IITs, IIITs, and some NITs. What matters is whether you enjoy the mathematical style, not just the institution name.",
            "\"You can skip the math and just focus on coding.\" — You can try, but you will miss the entire point of the branch and struggle in the courses that matter most.",
            "\"It is a niche branch with limited career options.\" — Quantitative computing roles (ML, fintech, algorithms, research) are among the highest-paying and most in-demand technical careers globally.",
        ],
        example_projects=[
            "Implementing a graph-based algorithm that optimizes delivery routes for a logistics company",
            "Building a recommendation engine using matrix factorization with mathematical analysis of why it works",
            "Developing a pricing optimization model that maximizes revenue for a dynamic pricing system",
            "Creating a Monte Carlo simulation to estimate financial risk in a portfolio of derivatives",
            "Implementing a zero-knowledge proof system for privacy-preserving identity verification",
        ],
        similar_branches=["Computer Science and Engineering", "Information Technology", "Engineering Physics"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Foundations \u2014 rigorous math and programming basics",
                        "courses": [
                                {
                                        "name": "Calculus & Real Analysis",
                                        "teaches": "Limits, continuity, sequences, series, multivariable calculus \u2014 more rigorous than standard engineering math",
                                        "tests": "Proof-based written exams; epsilon-delta style problems alongside computation"
                                },
                                {
                                        "name": "Linear Algebra",
                                        "teaches": "Vector spaces, eigenvalues, orthogonality, matrix decompositions \u2014 the math behind data and algorithms",
                                        "tests": "Theory and computation exams; proof problems on vector space properties"
                                },
                                {
                                        "name": "Introduction to Programming",
                                        "teaches": "C/Python programming, recursion, basic data structures \u2014 coding foundations",
                                        "tests": "Lab exams writing programs under time pressure; written logic exam"
                                },
                                {
                                        "name": "Engineering Physics",
                                        "teaches": "Mechanics, waves, basic quantum \u2014 general science foundation",
                                        "tests": "Theory exam plus physics lab practicals"
                                },
                                {
                                        "name": "Discrete Mathematics",
                                        "teaches": "Logic, sets, relations, functions, counting, graph theory \u2014 started earlier than typical CS programs",
                                        "tests": "Proof-heavy written exam; problem sets requiring formal mathematical arguments"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Mathematical depth and computing core",
                        "courses": [
                                {
                                        "name": "Probability & Statistics",
                                        "teaches": "Probability theory, distributions, estimation, hypothesis testing \u2014 rigorous statistical foundations",
                                        "tests": "Problem sets combining theory and computation; statistics lab using R or Python"
                                },
                                {
                                        "name": "Data Structures & Algorithms",
                                        "teaches": "Standard structures plus algorithm analysis with mathematical rigor \u2014 complexity proofs and design",
                                        "tests": "Coding assignments; algorithm design exams with proof requirements"
                                },
                                {
                                        "name": "Abstract Algebra (or Number Theory)",
                                        "teaches": "Groups, rings, fields \u2014 algebraic structures used in cryptography and coding theory",
                                        "tests": "Proof-based written exams; algebraic structure problem sets"
                                },
                                {
                                        "name": "Object-Oriented Programming",
                                        "teaches": "Java/C++ OOP, design patterns, software architecture principles",
                                        "tests": "Coding projects and lab exams; design pattern application assignments"
                                },
                                {
                                        "name": "Numerical Methods",
                                        "teaches": "Root finding, interpolation, numerical integration, ODE solvers \u2014 computing approximate solutions",
                                        "tests": "Numerical computation labs; written exam on method analysis and error bounds"
                                },
                                {
                                        "name": "Optimization",
                                        "teaches": "Linear programming, convex optimization, duality \u2014 mathematical frameworks for finding best solutions",
                                        "tests": "LP formulation and solving problems; optimization project with real-world data"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Advanced mathematics meets advanced computing",
                        "courses": [
                                {
                                        "name": "Stochastic Processes",
                                        "teaches": "Markov chains, Poisson processes, queuing theory \u2014 randomness with structure",
                                        "tests": "Probability modeling problems; simulation assignments using Python"
                                },
                                {
                                        "name": "Design and Analysis of Algorithms",
                                        "teaches": "Advanced algorithm design, approximation algorithms, randomized algorithms, NP-hardness proofs",
                                        "tests": "Algorithm design exams requiring correctness proofs and complexity analysis"
                                },
                                {
                                        "name": "Mathematical Logic & Computability",
                                        "teaches": "Propositional and predicate logic, Turing machines, decidability, G\u00f6del's theorems",
                                        "tests": "Formal proof exams; computability and decidability problems"
                                },
                                {
                                        "name": "Cryptography",
                                        "teaches": "Number-theoretic protocols, RSA, elliptic curves, hash functions, zero-knowledge proofs",
                                        "tests": "Cryptographic protocol analysis; implementation project; security proof assignments"
                                },
                                {
                                        "name": "Operating Systems / Computer Networks",
                                        "teaches": "Systems fundamentals shared with CS \u2014 process management, networking, distributed systems",
                                        "tests": "Written exams and programming assignments similar to CS curriculum"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Specialization and capstone",
                        "courses": [
                                {
                                        "name": "Machine Learning Theory (elective)",
                                        "teaches": "PAC learning, VC dimension, kernel methods, optimization for ML \u2014 the math behind ML algorithms",
                                        "tests": "Theoretical analysis assignments; ML implementation project with mathematical justification"
                                },
                                {
                                        "name": "Mathematical Finance (elective)",
                                        "teaches": "Stochastic calculus, Black-Scholes, portfolio theory, risk measures \u2014 quantitative finance foundations",
                                        "tests": "Option pricing and portfolio problems; simulation project"
                                },
                                {
                                        "name": "Operations Research (elective)",
                                        "teaches": "Integer programming, network flows, game theory, combinatorial optimization \u2014 industrial math",
                                        "tests": "Formulation and solving problems; OR case study project"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "Research-grade project combining mathematical analysis and computing implementation",
                                        "tests": "Mathematical results presentation, working code demo, written thesis, viva"
                                }
                        ]
                }
        ],
    ),
    CourseExplainer(
        name="Engineering Physics",
        slug="engineering-physics",
        family="advanced",
        overview="A physics-heavy branch for students who want analytical depth, devices, instrumentation, advanced systems, and specialized technical directions. Engineering Physics lives at the frontier where theoretical understanding meets applied engineering — designed for students who find mainstream branches too surface-level.",
        who_this_fits="students who genuinely enjoy physics and want engineering applications built on deep analytical foundations — not students chasing the most popular label",
        eli10="You use serious physics to understand and build real systems and devices — lasers, sensors, advanced materials, quantum devices, and precision instruments. Not just solving textbook problems for emotional damage, but actually using physics to engineer things that matter.",
        school_connection="If physics was your favorite subject — not because it was easy, but because understanding how the universe works felt genuinely exciting — Engineering Physics takes that love of physics into real engineering applications.",
        reality_check="Engineering Physics is not for students who need an obvious, mass-market career narrative. It is for students who care about depth, analytical foundations, and specialized upside more than easy explainability to relatives at family weddings.",
        choose_if="Choose Engineering Physics if you love physics-heavy thinking and want a branch that can feed into R&D, advanced devices, instrumentation, semiconductor physics, or research-driven engineering careers.",
        avoid_if="Avoid it if you need the most mainstream placement narrative, or if difficult abstraction drains your energy instead of fueling it.",
        what_you_study=[
            "Classical and quantum mechanics, electrodynamics, and statistical physics — deeper than most engineering branches go",
            "Optics, photonics, and laser physics — how light gets engineered for communication, measurement, and manufacturing",
            "Solid-state physics and semiconductor physics — the foundations behind chips, LEDs, solar cells, and sensors",
            "Mathematical physics and computational methods — serious modeling tools for complex systems",
            "Instrumentation, measurement science, and experimental techniques — how to precisely observe and quantify physical phenomena",
            "Electives in nanotechnology, materials physics, nuclear science, astrophysics applications, or quantum computing depending on college",
        ],
        problems_and_work=[
            "Designing optical systems, laser-based instruments, or photonic devices for communication or manufacturing",
            "Working on semiconductor device physics — understanding and improving how transistors, sensors, and LEDs work at the atomic level",
            "Building precision measurement and instrumentation systems for scientific, industrial, or medical applications",
            "Conducting R&D on advanced materials, thin films, or nanotechnology for next-generation products",
            "Modeling complex physical systems computationally — thermal, optical, electromagnetic, or quantum simulations",
            "Working in national laboratories, research institutions, or advanced technology companies on frontier problems",
        ],
        roles=[
            "R&D Engineer — working on advanced technology development in labs or technology companies",
            "Device Physicist / Semiconductor Engineer — working on chip design at the physics level (not just EDA tools)",
            "Instrumentation Engineer — designing precision measurement and control systems",
            "Optics / Photonics Engineer — working with lasers, fiber optics, imaging, or optical communication",
            "Research Scientist (post higher studies) — working on frontier physics and engineering problems in academia or industry labs",
            "Data Scientist / Quantitative Analyst — leveraging the strong analytical and mathematical foundations in non-traditional roles",
        ],
        tradeoffs=[
            "The branch is often misunderstood because its outcomes are less obvious to casual observers and family WhatsApp groups",
            "Higher studies (MS, PhD) can significantly amplify the career ceiling — B.Tech alone may feel limiting in some directions",
            "Mainstream campus placements may not fully reflect the branch's real potential — the best opportunities often come through research, internships, or specialized networks",
            "You need genuine intellectual curiosity to thrive — this branch does not reward passive consumption of lecture slides",
        ],
        good_fit_checklist=[
            "I genuinely enjoy physics-heavy thinking and find it energizing rather than draining",
            "I can handle abstract and mathematically demanding concepts without panicking",
            "I am open to specialized, research-oriented, or frontier-technology career paths",
            "I care more about depth and fit than mainstream branch popularity",
            "I am willing to invest in higher studies if that significantly improves my trajectory",
            "I find the idea of working on things like quantum devices, lasers, or semiconductor physics exciting",
        ],
        misconceptions=[
            "\"Engineering Physics is just physics BSc with extra steps.\" — It is explicitly engineered to bridge physics foundations with applied technology development. The engineering mindset is central.",
            "\"There are no placements.\" — Many EP graduates go into semiconductor companies, research labs, tech firms, consulting, and quantitative roles. The placements are different, not absent.",
            "\"You have to do a PhD to survive.\" — A PhD amplifies EP outcomes significantly, but B.Tech graduates also find roles in instrumentation, semiconductor, and analytical positions.",
            "\"Only IIT students should take this.\" — The branch is offered mainly at IITs, but the relevant question is whether you love physics enough to do it justice, not just whether you cleared a cutoff.",
            "\"EP graduates cannot work in software.\" — Many do, often bringing stronger mathematical and analytical foundations than typical CS graduates. But software should be a choice, not a fallback from disappointment.",
        ],
        example_projects=[
            "Designing an optical fiber-based sensor system for real-time temperature monitoring in industrial environments",
            "Simulating electron transport in a novel semiconductor nanostructure using computational physics tools",
            "Building a laser interferometry setup to measure surface roughness at nanometer precision",
            "Developing a thin-film solar cell prototype and characterizing its efficiency under different conditions",
            "Creating a Monte Carlo simulation of neutron transport for a nuclear reactor shielding analysis",
        ],
        similar_branches=["Electrical Engineering", "Metallurgical and Materials Engineering", "Mathematics and Computing"],
        year_by_year=[
                {
                        "year": 1,
                        "theme": "Rigorous foundations \u2014 physics and math at higher depth",
                        "courses": [
                                {
                                        "name": "Physics I: Classical Mechanics",
                                        "teaches": "Lagrangian mechanics, Hamiltonian formulation, central forces \u2014 deeper than standard engineering physics",
                                        "tests": "Problem-solving exams requiring Lagrangian/Hamiltonian approaches; derivation-heavy"
                                },
                                {
                                        "name": "Mathematics I & II",
                                        "teaches": "Real analysis, linear algebra, complex analysis \u2014 math at higher rigor than standard engineering",
                                        "tests": "Proof-based and computational exams; more mathematical maturity expected"
                                },
                                {
                                        "name": "Introduction to Programming",
                                        "teaches": "Python/C programming with emphasis on scientific computing and numerical methods",
                                        "tests": "Scientific computing lab exams; physics simulation assignments"
                                },
                                {
                                        "name": "Chemistry / Materials Basics",
                                        "teaches": "Atomic structure, bonding, material properties \u2014 chemistry relevant to device physics",
                                        "tests": "Written exam plus chemistry lab"
                                },
                                {
                                        "name": "Engineering Drawing / Workshop",
                                        "teaches": "Technical drawing, basic instrumentation fabrication, optical bench assembly",
                                        "tests": "Drawing sheets and lab practical assessment"
                                }
                        ]
                },
                {
                        "year": 2,
                        "theme": "Core physics \u2014 quantum mechanics, electrodynamics, and optics",
                        "courses": [
                                {
                                        "name": "Quantum Mechanics",
                                        "teaches": "Schr\u00f6dinger equation, hydrogen atom, angular momentum, perturbation theory \u2014 the physics of the very small",
                                        "tests": "Problem-solving exams with derivations; quantum mechanics problem sets"
                                },
                                {
                                        "name": "Electrodynamics",
                                        "teaches": "Maxwell's equations in full, electromagnetic wave propagation, radiation, waveguides",
                                        "tests": "Derivation-heavy written exams; computational electromagnetics assignments"
                                },
                                {
                                        "name": "Mathematical Physics",
                                        "teaches": "Complex analysis, special functions, Fourier analysis, Green's functions, tensor analysis",
                                        "tests": "Mathematical derivation exams; problem sets on special functions and transforms"
                                },
                                {
                                        "name": "Optics & Photonics",
                                        "teaches": "Wave optics, interference, diffraction, lasers, fiber optics, optical instruments",
                                        "tests": "Optics lab (interferometry, spectroscopy); written exam on wave optics theory"
                                },
                                {
                                        "name": "Thermal & Statistical Physics",
                                        "teaches": "Thermodynamic potentials, ensembles, partition functions, quantum statistics \u2014 connecting micro to macro",
                                        "tests": "Statistical mechanics problem solving; derivation of macroscopic properties from microscopic models"
                                }
                        ]
                },
                {
                        "year": 3,
                        "theme": "Solid state, devices, and computational physics",
                        "courses": [
                                {
                                        "name": "Solid State Physics",
                                        "teaches": "Crystal structure, phonons, electronic band theory, semiconductors, magnetic materials \u2014 matter in bulk",
                                        "tests": "Band structure calculation problems; solid state lab (Hall effect, resistivity measurements)"
                                },
                                {
                                        "name": "Semiconductor Device Physics",
                                        "teaches": "p-n junctions, MOSFETs, LEDs, solar cells, device fabrication \u2014 how electronic devices work at physics level",
                                        "tests": "Device analysis problems; semiconductor characterization lab"
                                },
                                {
                                        "name": "Laser Physics & Applications",
                                        "teaches": "Stimulated emission, laser systems, nonlinear optics, laser applications in industry and medicine",
                                        "tests": "Laser lab experiments; written exam on laser theory and applications"
                                },
                                {
                                        "name": "Computational Physics",
                                        "teaches": "Monte Carlo methods, molecular dynamics, PDE solvers, scientific visualization \u2014 physics through simulation",
                                        "tests": "Computational projects simulating physical systems; code review and results analysis"
                                },
                                {
                                        "name": "Instrumentation & Measurement",
                                        "teaches": "Sensors, data acquisition, signal conditioning, error analysis \u2014 precision measurement for science",
                                        "tests": "Instrumentation lab with real measurement systems; error analysis reports"
                                }
                        ]
                },
                {
                        "year": 4,
                        "theme": "Frontier topics and capstone",
                        "courses": [
                                {
                                        "name": "Nanotechnology & Nanomaterials (elective)",
                                        "teaches": "Quantum dots, thin films, nanostructure fabrication, characterization at nanoscale",
                                        "tests": "Nanofabrication lab or simulation project; literature review presentation"
                                },
                                {
                                        "name": "Nuclear & Particle Physics (elective)",
                                        "teaches": "Nuclear structure, radioactivity, particle interactions, detector physics \u2014 subatomic world",
                                        "tests": "Nuclear physics problems; radiation measurement lab"
                                },
                                {
                                        "name": "Quantum Computing Basics (elective)",
                                        "teaches": "Qubits, quantum gates, entanglement, quantum algorithms \u2014 computing with quantum mechanics",
                                        "tests": "Quantum circuit design problems; simulation project using Qiskit or similar"
                                },
                                {
                                        "name": "Capstone Project / B.Tech Thesis",
                                        "teaches": "Physics research project: experimental or computational, requiring original analysis and results",
                                        "tests": "Research presentation, written thesis with data analysis, viva with external examiner"
                                }
                        ]
                }
        ],
    ),
]


class CourseExplainerService:
    def all_courses(self) -> list[CourseExplainer]:
        return list(TOP_12_COURSES)

    def popular_courses(self, limit: int = 12) -> list[CourseExplainer]:
        return self.all_courses()[:limit]

    def get_by_slug(self, slug: str) -> CourseExplainer | None:
        return next((course for course in TOP_12_COURSES if course.slug == slug), None)
