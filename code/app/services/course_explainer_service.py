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
    reality_check: str
    choose_if: str
    avoid_if: str
    what_you_study: list[str]
    problems_and_work: list[str]
    roles: list[str]
    tradeoffs: list[str]
    good_fit_checklist: list[str]
    similar_branches: list[str]


TOP_12_COURSES: list[CourseExplainer] = [
    CourseExplainer(
        name="Computer Science and Engineering",
        slug="computer-science-and-engineering",
        family="computing",
        overview="The broadest software-oriented branch: code, systems, algorithms, data, and the foundations behind modern digital products.",
        who_this_fits="students who genuinely enjoy coding, abstraction, logic, and building digital products or systems",
        eli10="You learn how computers think, how software gets built, and how to make apps, tools, and systems that solve real problems.",
        reality_check="This branch creates a lot of opportunity, but it also attracts a lot of tourists. If you do not actually enjoy coding, the hype wears off fast and you end up competing in the most crowded lane anyway.",
        choose_if="choose CSE if you want the widest software flexibility and you like solving problems by thinking through code, architecture, and logic",
        avoid_if="avoid CSE if you are choosing it only because everyone told you it is the safest option, while you secretly dislike long hours of debugging and iterative technical learning",
        what_you_study=[
            "programming, data structures, algorithms, and software engineering fundamentals",
            "operating systems, databases, networks, compilers, and system-level thinking",
            "math foundations that support computation, optimization, and machine reasoning",
        ],
        problems_and_work=[
            "building apps, internal tools, APIs, backend systems, and product infrastructure",
            "improving performance, reliability, developer velocity, and software quality",
            "solving digital product problems where code is the main tool of execution",
        ],
        roles=["software engineer", "backend or full-stack engineer", "platform engineer", "developer infrastructure engineer"],
        tradeoffs=[
            "competition is brutally high because the branch is crowded and heavily marketed",
            "your degree helps, but projects, internships, and problem-solving depth matter far more after a point",
            "the field changes fast, so comfort with continuous learning is not optional",
        ],
        good_fit_checklist=[
            "I enjoy coding even when it becomes frustrating",
            "I like logic and structured problem solving",
            "I want broad digital career flexibility",
            "I can handle constant upskilling without romantic drama about it",
        ],
        similar_branches=["Information Technology", "Mathematics and Computing", "Electronics and Communication Engineering"],
    ),
    CourseExplainer(
        name="Mechanical Engineering",
        slug="mechanical-engineering",
        family="mechanical",
        overview="The branch of machines, motion, manufacturing, thermal systems, design, and physical engineering intuition.",
        who_this_fits="students who like machines, mechanisms, physical products, manufacturing, and seeing engineering become tangible",
        eli10="You learn how machines move, how engines and systems work, and how to design things that do useful physical work in the real world.",
        reality_check="Mechanical is not 'old' engineering. It is foundational engineering. The real issue is that students often expect prestige to carry them, when the branch rewards hands-on depth, internships, and specialization.",
        choose_if="choose Mechanical if you enjoy physical systems, design, manufacturing, robotics-adjacent work, or understanding how real products and machines behave",
        avoid_if="avoid Mechanical if you want the easiest path to a generic laptop-only career and do not care much about real-world hardware or industrial systems",
        what_you_study=[
            "mechanics, thermodynamics, fluids, materials, manufacturing, and machine design",
            "how forces, heat, motion, stress, and efficiency affect engineered systems",
            "analysis and simulation used to design and validate physical products",
        ],
        problems_and_work=[
            "designing components, machines, production systems, and thermal solutions",
            "improving efficiency, reliability, manufacturability, and maintenance outcomes",
            "working in design, testing, operations, production, automotive, or industrial environments",
        ],
        roles=["design engineer", "manufacturing engineer", "automotive engineer", "production or operations engineer"],
        tradeoffs=[
            "core opportunities can be more location-dependent than mainstream software roles",
            "you usually need internships, CAD/design exposure, or domain depth to stand out",
            "some roles are extremely practical and execution-heavy, not just theoretical",
        ],
        good_fit_checklist=[
            "I enjoy physical systems more than purely digital systems",
            "I like understanding how things move, fail, and get built",
            "I can handle practical constraints, not just elegant classroom answers",
            "I can imagine working with hardware, plants, labs, or manufacturing teams",
        ],
        similar_branches=["Industrial Engineering", "Aerospace Engineering", "Civil Engineering"],
    ),
    CourseExplainer(
        name="Electronics and Communication Engineering",
        slug="electronics-and-communication-engineering",
        family="electronics",
        overview="A strong hybrid branch covering circuits, signals, communication systems, embedded systems, and hardware-software interfaces.",
        who_this_fits="students who like electronics, systems, and want flexibility across hardware, embedded, telecom, and some software paths",
        eli10="You learn how devices talk, how signals move, and how electronic systems get designed so networks, smart devices, and communication systems actually work.",
        reality_check="ECE is one of the most misunderstood branches because students see the upside but underestimate the signal processing, math, and hardware depth. It is versatile — but not effortless.",
        choose_if="choose ECE if you want a branch that keeps hardware depth while still allowing pathways into embedded systems, semiconductor-adjacent work, and even software later",
        avoid_if="avoid ECE if you dislike circuits and mathematically heavy engineering and are only picking it because it sounds close enough to CSE",
        what_you_study=[
            "circuits, analog and digital electronics, communication systems, and signal processing",
            "embedded systems, devices, control concepts, and real-world electronic behavior",
            "mathematical analysis used to understand signals, noise, transmission, and system performance",
        ],
        problems_and_work=[
            "building and testing embedded systems, communication hardware, or electronic subsystems",
            "working on firmware, devices, telecom systems, or hardware-linked product engineering",
            "bridging physical electronics with programmable system behavior",
        ],
        roles=["embedded engineer", "electronics design engineer", "signal processing engineer", "telecom or systems engineer"],
        tradeoffs=[
            "it can feel harder than students expect because the branch mixes abstraction with real hardware constraints",
            "core roles often need stronger specialization than generic software placement tracks",
            "many students drift into software because they never build confidence in the electronics side",
        ],
        good_fit_checklist=[
            "I like circuits, devices, or signal-heavy systems",
            "I am okay with serious math in engineering",
            "I want flexibility between hardware and software-adjacent paths",
            "I care about how systems work beneath the interface layer",
        ],
        similar_branches=["Electrical Engineering", "Electrical and Electronics Engineering", "Instrumentation Engineering"],
    ),
    CourseExplainer(
        name="Civil Engineering",
        slug="civil-engineering",
        family="civil",
        overview="The branch behind roads, bridges, buildings, transport systems, water systems, and the physical backbone of society.",
        who_this_fits="students who want visible real-world impact through structures, infrastructure, transport, and city-scale engineering",
        eli10="You help design the things cities are made of — buildings, roads, bridges, water systems, and infrastructure people use every day.",
        reality_check="Civil is often underrated by students who confuse online glamour with real-world importance. The branch matters enormously; the key is whether you actually want infrastructure work, site realities, and long project cycles.",
        choose_if="choose Civil if you care about buildings, transport, urban systems, construction, or physical infrastructure with visible long-term impact",
        avoid_if="avoid Civil if you want everything to be fast, remote, clean, and digitally abstract with minimal site or execution exposure",
        what_you_study=[
            "structures, geotechnical engineering, transportation, water resources, and construction systems",
            "how loads, soil, materials, drainage, and standards shape safety and durability",
            "project planning and execution constraints in large physical systems",
        ],
        problems_and_work=[
            "designing and evaluating structures, roads, water systems, and site plans",
            "managing construction quality, execution, coordination, and engineering compliance",
            "solving public infrastructure and built-environment problems under cost and safety constraints",
        ],
        roles=["structural engineer", "site or construction engineer", "transportation engineer", "water resources engineer"],
        tradeoffs=[
            "field and site work can be demanding depending on the role and employer",
            "career growth often depends on execution experience, not just academic marks",
            "projects can move slower than digital product cycles, but the impact is more tangible",
        ],
        good_fit_checklist=[
            "I care about physical infrastructure and the built environment",
            "I can handle practical constraints and long project timelines",
            "I do not need a fully desk-bound career",
            "I find visible real-world impact motivating",
        ],
        similar_branches=["Mechanical Engineering", "Environmental Engineering", "Architecture-adjacent planning paths"],
    ),
    CourseExplainer(
        name="Electrical Engineering",
        slug="electrical-engineering",
        family="electronics",
        overview="Power, machines, control, energy systems, and the engineering of electrical infrastructure at real scale.",
        who_this_fits="students who like power systems, control, mathematically grounded engineering, and infrastructure-heavy technical work",
        eli10="You learn how electricity gets generated, controlled, and used in real systems — from motors and grids to industrial equipment and control systems.",
        reality_check="Electrical is a serious branch with real industrial relevance, but it is less socially hyped than software. That scares students off even when the actual engineering fit is much stronger for them.",
        choose_if="choose Electrical if you like energy, control systems, machines, infrastructure, and engineering that touches the real physical world at scale",
        avoid_if="avoid Electrical if you dislike physics-heavy analytical work and want only trendy narratives with instant gratification",
        what_you_study=[
            "circuits, electrical machines, power systems, control systems, and core electrical analysis",
            "how energy flows through systems and how those systems are managed and protected",
            "mathematical modeling of electrical and dynamic system behavior",
        ],
        problems_and_work=[
            "power distribution, control systems, drives, industrial systems, and electrical design",
            "working on plants, substations, motors, automation, or electrical infrastructure",
            "improving reliability, safety, and efficiency of electrical systems",
        ],
        roles=["power systems engineer", "control engineer", "electrical design engineer", "industrial systems engineer"],
        tradeoffs=[
            "the theory can feel intense if you do not genuinely like physics and math",
            "some of the best roles are domain-specific rather than generic campus-brand prestige roles",
            "you may need patience to appreciate the branch if you compare everything against software salaries on day one",
        ],
        good_fit_checklist=[
            "I like power, systems, or industrial engineering",
            "I am comfortable with analytical rigor",
            "I care about infrastructure and control systems",
            "I want engineering depth, not just the most fashionable label",
        ],
        similar_branches=["Electrical and Electronics Engineering", "Electronics and Communication Engineering", "Engineering Physics"],
    ),
    CourseExplainer(
        name="Chemical Engineering",
        slug="chemical-engineering",
        family="process",
        overview="The engineering of industrial processes — turning raw materials into useful products safely, efficiently, and at scale.",
        who_this_fits="students who enjoy chemistry-linked systems, plants, production, process thinking, and large-scale transformation",
        eli10="You learn how factories turn raw materials into useful things at huge scale without wasting energy, blowing up, or producing garbage outcomes.",
        reality_check="Chemical Engineering is not just class-12 chemistry with better branding. It is about process systems, scale, heat, flow, safety, and industrial optimization. Students who miss that difference get confused quickly.",
        choose_if="choose Chemical if you like industrial systems, process thinking, scale-up problems, and the idea of engineering how products get made",
        avoid_if="avoid Chemical if you want a light branch or if the only reason you are choosing it is because you scored well in school chemistry",
        what_you_study=[
            "thermodynamics, reaction engineering, transport phenomena, and process design",
            "how materials flow, react, separate, heat, and transform in industrial systems",
            "optimization, plant safety, and scale-up thinking for production environments",
        ],
        problems_and_work=[
            "improving process efficiency, quality, yield, and safety in industrial settings",
            "working on plant operations, production, process design, or energy-linked systems",
            "turning lab concepts into scalable, economically viable manufacturing processes",
        ],
        roles=["process engineer", "plant engineer", "production engineer", "energy or manufacturing roles"],
        tradeoffs=[
            "some roles are plant-heavy and location-specific",
            "the branch is great for the right student but confusing for those expecting generic office work",
            "higher upside often comes from domain strength, not branch-name prestige alone",
        ],
        good_fit_checklist=[
            "I like process thinking and large-scale systems",
            "I do not mind industry-facing or plant-facing work",
            "I am curious about how products get manufactured at scale",
            "I want engineering that mixes science with operations",
        ],
        similar_branches=["Metallurgical and Materials Engineering", "Bio Technology", "Petroleum or process-linked branches"],
    ),
    CourseExplainer(
        name="Metallurgical and Materials Engineering",
        slug="metallurgical-and-materials-engineering",
        family="materials",
        overview="The branch that studies what things are made of, how materials behave, and how better material choices improve engineering outcomes.",
        who_this_fits="students who are curious about metals, alloys, materials behavior, manufacturing, and why things fail or survive",
        eli10="You learn why some metals bend, some crack, some survive heat, and why choosing the right material can make or break an engineering system.",
        reality_check="This branch sounds narrow to outsiders, but materials thinking shows up everywhere: manufacturing, automotive, aerospace, electronics, energy, and failure analysis. The branch is often underestimated because the name sounds old-school.",
        choose_if="choose this branch if you enjoy applied science inside engineering and want to understand strength, durability, processing, and performance deeply",
        avoid_if="avoid it if you need a branch with instantly obvious brand recognition and have zero interest in materials, industry, or manufacturing depth",
        what_you_study=[
            "metals, alloys, phase behavior, corrosion, heat treatment, and material properties",
            "how internal structure changes strength, toughness, durability, and performance",
            "materials selection for engineering design, processing, and production",
        ],
        problems_and_work=[
            "improving material performance, product reliability, and failure resistance",
            "working in steel, manufacturing, testing, quality, or process-linked environments",
            "supporting product decisions where material behavior directly affects outcomes",
        ],
        roles=["materials engineer", "metallurgy engineer", "quality or failure-analysis engineer", "manufacturing and process roles"],
        tradeoffs=[
            "students often dismiss it before understanding what the work actually looks like",
            "the branch can feel specialized compared with generic computing careers",
            "the best outcomes usually come when you lean into the domain instead of apologizing for it",
        ],
        good_fit_checklist=[
            "I like understanding what products are made of and why that matters",
            "I enjoy applied science more than superficial trend-following",
            "I can appreciate specialized industrial domains",
            "I do not need mass-market prestige to stay confident in my path",
        ],
        similar_branches=["Chemical Engineering", "Mechanical Engineering", "Engineering Physics"],
    ),
    CourseExplainer(
        name="Electrical and Electronics Engineering",
        slug="electrical-and-electronics-engineering",
        family="electronics",
        overview="A blend of electrical systems and electronics, often sitting between power-oriented and device-oriented engineering.",
        who_this_fits="students who want overlap between electrical systems and electronics rather than a narrowly pure path in only one direction",
        eli10="You learn both the bigger electrical world and the smaller electronics world, so you can work on systems that use both.",
        reality_check="EEE can be very useful, but it is one of those branches where your actual projects and electives matter a lot. If you drift, the branch feels vague. If you shape it well, it becomes genuinely versatile.",
        choose_if="choose EEE if you want a middle ground between electrical infrastructure thinking and electronics/system-level engineering",
        avoid_if="avoid EEE if you need a hyper-clean branch identity and do not want to actively shape your own direction through projects and electives",
        what_you_study=[
            "electrical fundamentals, circuits, electronics, machines, and control concepts",
            "a blend of power-oriented and device-oriented engineering topics",
            "applied systems thinking across electrical and electronic behavior",
        ],
        problems_and_work=[
            "working on automation, equipment, control panels, electronics-linked systems, and industrial hardware",
            "supporting environments where electrical infrastructure and electronic subsystems overlap",
            "bridging practical hardware layers rather than staying in one narrow silo",
        ],
        roles=["EEE engineer", "control and automation engineer", "industrial electronics engineer", "systems or plant engineer"],
        tradeoffs=[
            "students can get confused about how it differs from EE or ECE unless they look at the curriculum closely",
            "the branch rewards self-direction more than passive expectation",
            "outcomes vary significantly based on college quality and practical exposure",
        ],
        good_fit_checklist=[
            "I want both electrical and electronics exposure",
            "I am okay with shaping my own focus area over time",
            "I like real systems that interact with the physical world",
            "I do not need everything to fit into a neat one-word identity",
        ],
        similar_branches=["Electrical Engineering", "Electronics and Communication Engineering", "Instrumentation Engineering"],
    ),
    CourseExplainer(
        name="Information Technology",
        slug="information-technology",
        family="computing",
        overview="A software-focused branch with strong overlap with CSE, often leaning a bit more toward applications, systems, databases, and practical computing.",
        who_this_fits="students who want software careers similar to CSE and care more about work fit than prestige hair-splitting",
        eli10="You learn how to build and manage software systems that help people and companies store information, run applications, and keep digital systems working.",
        reality_check="The internet loves dramatic CSE-vs-IT debates. In practice, the difference often matters less than college quality, your projects, and whether you can actually code well under real constraints.",
        choose_if="choose IT if you want practical software roles and are comfortable with a branch that often overlaps substantially with CSE outcomes",
        avoid_if="avoid IT if you are going to spend four years feeling inferior about the label instead of building skill, because that is a self-own of legendary proportions",
        what_you_study=[
            "programming, databases, networking, web systems, and software engineering",
            "application-oriented computing topics that support product and enterprise software work",
            "many concepts that overlap strongly with CSE depending on the institution",
        ],
        problems_and_work=[
            "building business software, applications, data systems, and web products",
            "working on APIs, backend logic, databases, and internal digital tools",
            "solving practical software problems in organizations and products",
        ],
        roles=["software engineer", "web or backend engineer", "data systems engineer", "application engineer"],
        tradeoffs=[
            "some students create unnecessary insecurity around the branch name",
            "the branch still demands real coding skill and project work",
            "outcomes can be excellent, but they are earned through execution not label anxiety",
        ],
        good_fit_checklist=[
            "I want software roles",
            "I am comfortable with coding-heavy learning",
            "I care more about actual work than semantic prestige debates",
            "I want broad practical computing options",
        ],
        similar_branches=["Computer Science and Engineering", "Mathematics and Computing", "Electronics and Communication Engineering"],
    ),
    CourseExplainer(
        name="Bio Technology",
        slug="bio-technology",
        family="bio",
        overview="A biology-plus-engineering branch for students interested in life sciences, biotech systems, health, lab work, and research-linked technical paths.",
        who_this_fits="students who genuinely like biology and want applied scientific or research-oriented engineering pathways",
        eli10="You use engineering ideas to work with living systems — cells, biological processes, biotech tools, and health-related technologies.",
        reality_check="Biotech can be powerful for the right student, but it is rarely the branch to choose casually. If you do not like biology, lab-heavy science, or the possibility of higher studies, you may hate the path.",
        choose_if="choose Bio Technology if you genuinely enjoy biology and are open to labs, scientific depth, and possibly higher-study-amplified outcomes",
        avoid_if="avoid it if you only want the safest mainstream placement story and have no real interest in biological systems or research-heavy work",
        what_you_study=[
            "molecular biology, genetics-linked topics, biological systems, and engineering applications",
            "how living systems can be analyzed, manipulated, or used in useful products and processes",
            "science-heavy and often lab-linked foundations compared with many core engineering branches",
        ],
        problems_and_work=[
            "working on biotech products, diagnostics, biological processes, or applied life-science systems",
            "supporting R&D, lab, process, or product work in biotech and health-linked environments",
            "building foundations for more specialized technical paths through higher studies or domain depth",
        ],
        roles=["biotech engineer", "R&D or lab-focused roles", "process roles in biotech or pharma contexts", "higher-study-oriented technical pathways"],
        tradeoffs=[
            "higher studies often matter more here than in mainstream software branches",
            "career paths can feel less obvious to students who want a plug-and-play trajectory",
            "it rewards genuine scientific interest more than surface-level branch chasing",
        ],
        good_fit_checklist=[
            "I actually enjoy biology",
            "I am open to labs, research, or higher studies",
            "I want science-heavy engineering rather than generic placements",
            "I am comfortable with a path that may be less mainstream but more specialized",
        ],
        similar_branches=["Biomedical Engineering", "Chemical Engineering", "Engineering Physics"],
    ),
    CourseExplainer(
        name="Mathematics and Computing",
        slug="mathematics-and-computing",
        family="computing",
        overview="A quantitatively intense branch combining abstract mathematics, algorithms, modeling, and advanced computing.",
        who_this_fits="students who enjoy abstract math, algorithms, and analytical computing more than generic software hype",
        eli10="It is like taking the math-heavy brain of computing and using it to solve harder software, data, optimization, and modeling problems.",
        reality_check="Math and Computing sounds glamorous because it overlaps with high-value technical work, but the math load is not decorative. Students who only want the status and not the abstraction can suffer spectacularly.",
        choose_if="choose this branch if you truly like mathematics and want computing with more analytical depth than the usual software storyline",
        avoid_if="avoid it if you hate abstract reasoning and only want software because it seems lucrative or socially impressive",
        what_you_study=[
            "discrete math, probability, proofs, optimization, algorithms, and programming",
            "mathematical reasoning that supports advanced computing and analytical systems",
            "a more quantitative and intellectually demanding flavor than generic computing tracks",
        ],
        problems_and_work=[
            "algorithm-heavy software work and mathematically demanding systems problems",
            "optimization, analytics, data, ML-adjacent, and quantitative computing tasks",
            "research-like or depth-heavy technical work where mathematical thinking matters materially",
        ],
        roles=["software engineer", "ML or data engineer", "quantitative computing roles", "research-oriented technical roles"],
        tradeoffs=[
            "the branch can be amazing for the right student and miserable for the wrong one",
            "math intensity creates a real filtering effect",
            "some people choose it for prestige and then discover abstraction was not their friend after all",
        ],
        good_fit_checklist=[
            "I truly like math, not just scoring in math",
            "I enjoy abstraction and analytical reasoning",
            "I want computing with more quantitative depth",
            "I can trade some comfort for stronger intellectual fit",
        ],
        similar_branches=["Computer Science and Engineering", "Information Technology", "Engineering Physics"],
    ),
    CourseExplainer(
        name="Engineering Physics",
        slug="engineering-physics",
        family="advanced",
        overview="A physics-heavy branch for students who want analytical depth, devices, instrumentation, advanced systems, and specialized technical directions.",
        who_this_fits="students who genuinely enjoy physics and want engineering applications rather than only mainstream branch branding",
        eli10="You use serious physics to understand and build real systems and devices — not just to solve textbook problems and collect emotional damage.",
        reality_check="Engineering Physics is not for students who need a very obvious mass-market branch narrative. It is for students who care about depth, analytical foundations, and specialized upside more than easy explainability to relatives.",
        choose_if="choose Engineering Physics if you love physics-heavy thinking and want a branch that can feed into advanced engineering, devices, instrumentation, or research-like directions",
        avoid_if="avoid it if you need the most mainstream placement narrative or if difficult abstraction drains you instead of energizing you",
        what_you_study=[
            "physics-heavy engineering foundations, mathematical modeling, and analytical technical systems",
            "devices, instrumentation, and scientific-system thinking with stronger theory depth",
            "foundations that can support specialized engineering, R&D, and higher-study-led pathways",
        ],
        problems_and_work=[
            "physics-heavy engineering problems where modeling and analytical depth matter",
            "instrumentation, devices, specialized systems, and technical R&D pathways",
            "building foundations for advanced engineering roles or further specialization",
        ],
        roles=["R&D engineer", "instrumentation or device-focused engineer", "specialized technical roles", "higher-study-oriented engineering paths"],
        tradeoffs=[
            "the branch is often misunderstood because its outcomes are less obvious to casual observers",
            "higher studies can significantly amplify the payoff",
            "it rewards curiosity and analytical stamina more than trend-following",
        ],
        good_fit_checklist=[
            "I genuinely enjoy physics-heavy thinking",
            "I can handle abstract concepts without panicking",
            "I am open to specialized or research-leaning paths",
            "I care more about fit than mainstream branch hype",
        ],
        similar_branches=["Electrical Engineering", "Metallurgical and Materials Engineering", "Mathematics and Computing"],
    ),
]


class CourseExplainerService:
    def all_courses(self) -> list[CourseExplainer]:
        return list(TOP_12_COURSES)

    def popular_courses(self, limit: int = 12) -> list[CourseExplainer]:
        return self.all_courses()[:limit]

    def get_by_slug(self, slug: str) -> CourseExplainer | None:
        return next((course for course in TOP_12_COURSES if course.slug == slug), None)
