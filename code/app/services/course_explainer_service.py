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
        overview="Build software systems, reason with algorithms, and work on digital products, platforms, and infrastructure.",
        who_this_fits="students who genuinely enjoy coding, logic, abstraction, and building digital things",
        eli10="You learn how computers think, how software gets built, and how to make apps, systems, and tools that solve real problems.",
        what_you_study=["programming, data structures, algorithms, and system design thinking", "computer networks, operating systems, databases, and software engineering", "math foundations that support computing, optimization, and machine reasoning"],
        problems_and_work=["building apps, platforms, internal tools, and scalable backend systems", "improving speed, reliability, and usability of software systems", "solving product and engineering problems where code is the main lever"],
        roles=["software engineer", "backend or full-stack engineer", "platform engineer", "developer tools or infrastructure engineer"],
        tradeoffs=["many students pick it for prestige without liking the actual work", "you still need projects, skill, and consistency — the degree name does not code for you", "competition is intense because the branch is crowded and hyped"],
        good_fit_checklist=["I enjoy coding for more than exam marks", "I like logic and debugging", "I want broad software career flexibility", "I am okay learning continuously because tech does not sit still"],
        similar_branches=["Information Technology", "Mathematics and Computing", "Electronics and Communication Engineering"],
    ),
    CourseExplainer(
        name="Mechanical Engineering",
        slug="mechanical-engineering",
        family="mechanical",
        overview="Design and analyze machines, motion, thermal systems, manufacturing processes, and physical products.",
        who_this_fits="students who like machines, mechanisms, physical systems, and seeing engineering become tangible",
        eli10="You figure out how machines move, how engines and systems work, and how to design things that do useful physical work.",
        what_you_study=["mechanics, thermodynamics, manufacturing, materials, and machine design", "how forces, heat, motion, and efficiency affect real systems", "engineering math used for design, analysis, and simulation of physical systems"],
        problems_and_work=["designing components, machines, and manufacturing systems", "improving efficiency, reliability, and maintainability of industrial systems", "working on production, design validation, testing, or plant-facing engineering"],
        roles=["design engineer", "manufacturing engineer", "automotive engineer", "operations or production engineer"],
        tradeoffs=["the branch is broad, so direction matters a lot", "core roles can be more location-dependent than software jobs", "you may need internships and specialization to stand out"],
        good_fit_checklist=["I enjoy physical systems more than purely digital work", "I like understanding how things move and fail", "I do not mind practical engineering constraints", "I can see myself in plants, labs, factories, or product design teams"],
        similar_branches=["Industrial Engineering", "Aerospace Engineering", "Civil Engineering"],
    ),
    CourseExplainer(
        name="Electronics and Communication Engineering",
        slug="electronics-and-communication-engineering",
        family="electronics",
        overview="Work with circuits, signals, communication systems, embedded systems, and hardware-software interfaces.",
        who_this_fits="students who like electronics, systems thinking, and want flexibility across hardware, embedded, and some software paths",
        eli10="You learn how devices talk, how signals move, and how electronic systems get designed so phones, networks, and smart devices actually work.",
        what_you_study=["circuits, communication systems, signal processing, and electronic devices", "embedded systems, control concepts, and hardware-facing problem solving", "math-heavy analysis used to understand noise, signals, and system behavior"],
        problems_and_work=["building and testing electronic systems and communication hardware", "working on embedded devices, network hardware, or chip-adjacent systems", "bridging hardware understanding with software control or firmware"],
        roles=["embedded engineer", "electronics design engineer", "signal processing engineer", "telecom or systems engineer"],
        tradeoffs=["students often underestimate the math and signal-heavy parts", "core hardware roles can require more specialization than generic software", "some people enter it planning to switch to software anyway"],
        good_fit_checklist=["I like circuits or electronic systems", "I am comfortable with math-heavy engineering", "I want some flexibility between hardware and software-adjacent paths", "I enjoy understanding how real devices work underneath the UI layer"],
        similar_branches=["Electrical Engineering", "Electrical and Electronics Engineering", "Instrumentation Engineering"],
    ),
    CourseExplainer(
        name="Civil Engineering",
        slug="civil-engineering",
        family="civil",
        overview="Plan, design, and build infrastructure: roads, bridges, buildings, water systems, and cities.",
        who_this_fits="students who want visible real-world impact through structures, transport, construction, and infrastructure",
        eli10="You help design the things cities are made of — buildings, roads, bridges, and systems people use every day without thinking about them.",
        what_you_study=["structures, geotechnical concepts, transportation, water resources, and construction systems", "how loads, soil, materials, and design standards affect safety and durability", "project planning and practical execution constraints in large physical systems"],
        problems_and_work=["designing and evaluating structures or infrastructure systems", "managing site execution, quality, and engineering coordination", "solving public-works and construction problems with safety, cost, and longevity tradeoffs"],
        roles=["structural engineer", "site or construction engineer", "transportation engineer", "water resources engineer"],
        tradeoffs=["field/site work can be demanding depending on role", "career growth often depends on execution experience, not just classroom theory", "it is less glamorous online than it is important in the real world"],
        good_fit_checklist=["I care about physical infrastructure and built environments", "I can handle practical constraints and long project cycles", "I do not need a laptop-only career", "I like visible impact in the real world"],
        similar_branches=["Mechanical Engineering", "Environmental Engineering", "Architecture-adjacent planning paths"],
    ),
    CourseExplainer(
        name="Electrical Engineering",
        slug="electrical-engineering",
        family="electronics",
        overview="Understand and build power systems, control systems, machines, and electrical infrastructure.",
        who_this_fits="students who like power, energy, systems, and mathematically grounded engineering",
        eli10="You learn how electricity gets generated, controlled, and used in real systems — from motors and grids to control-heavy industrial equipment.",
        what_you_study=["circuits, electrical machines, power systems, and control theory", "how energy moves through systems and how those systems are analyzed and protected", "math-heavy modeling of electrical behavior and dynamic systems"],
        problems_and_work=["power distribution, control systems, industrial systems, and electrical design", "working on motors, drives, substations, grid equipment, or plant systems", "improving reliability and safety of electrical infrastructure"],
        roles=["power systems engineer", "control engineer", "electrical design engineer", "industrial systems engineer"],
        tradeoffs=["the branch is strong but less hyped than computing, so students misread it", "core roles may be domain-specific rather than universally flexible", "theory can feel intense if you do not actually like physics and math"],
        good_fit_checklist=["I like power, systems, or industrial engineering", "I am okay with analytical rigor", "I care about real infrastructure and control systems", "I want engineering depth, not just branch-name trendiness"],
        similar_branches=["Electrical and Electronics Engineering", "Electronics and Communication Engineering", "Engineering Physics"],
    ),
    CourseExplainer(
        name="Chemical Engineering",
        slug="chemical-engineering",
        family="process",
        overview="Design and optimize industrial processes that transform raw materials into useful products at scale.",
        who_this_fits="students who enjoy chemistry-linked systems, industrial processes, and large-scale production thinking",
        eli10="You learn how factories turn raw materials into useful things safely, efficiently, and at huge scale.",
        what_you_study=["thermodynamics, reaction engineering, transport phenomena, and process design", "how materials flow, react, separate, heat, and change inside industrial systems", "optimization and safety thinking for plant-scale engineering"],
        problems_and_work=["improving industrial process efficiency and yield", "working on plant operations, safety, quality, or process design", "solving scale-up problems where lab ideas become real manufacturing systems"],
        roles=["process engineer", "plant engineer", "production engineer", "energy, chemicals, or manufacturing roles"],
        tradeoffs=["it is not just class-12 chemistry in a hard hat", "some roles are plant-heavy and location-specific", "students who want a generic office job often misunderstand the branch"],
        good_fit_checklist=["I like process thinking and large-scale systems", "I do not mind industry-facing or plant-facing roles", "I am curious about how products get made at scale", "I want engineering that mixes science with operations"],
        similar_branches=["Metallurgical and Materials Engineering", "Biotechnology", "Petroleum or process-linked branches"],
    ),
    CourseExplainer(
        name="Metallurgical and Materials Engineering",
        slug="metallurgical-and-materials-engineering",
        family="materials",
        overview="Study how materials behave, fail, strengthen, and get selected for engineering use.",
        who_this_fits="students curious about why materials behave differently and how that changes real engineering decisions",
        eli10="You learn why some metals bend, some crack, some survive heat, and why choosing the right material can make or break an engineering system.",
        what_you_study=["metals, alloys, phase behavior, heat treatment, and material properties", "how structure at small scales changes strength, durability, corrosion, and performance", "materials selection for manufacturing, design, and industrial use"],
        problems_and_work=["improving material performance and failure resistance", "working in steel, metals, manufacturing, testing, or quality systems", "supporting product and process decisions through materials understanding"],
        roles=["materials engineer", "metallurgy engineer", "quality or failure-analysis engineer", "manufacturing and process roles"],
        tradeoffs=["students often ignore it because the name sounds narrow", "the upside is strong for people who genuinely like materials and industry", "some roles may feel specialized compared with broad software careers"],
        good_fit_checklist=["I like understanding what things are made of", "I enjoy applied science inside engineering", "I can appreciate specialized industrial domains", "I do not need mass-market branch prestige to stay confident"],
        similar_branches=["Chemical Engineering", "Mechanical Engineering", "Engineering Physics"],
    ),
    CourseExplainer(
        name="Electrical and Electronics Engineering",
        slug="electrical-and-electronics-engineering",
        family="electronics",
        overview="Mix electrical systems with electronics, devices, and applied control-oriented engineering.",
        who_this_fits="students who want overlap between electrical systems and electronics rather than a purely power-focused path",
        eli10="This is where power systems and electronics shake hands — you learn both the bigger electrical world and the smaller device-level world.",
        what_you_study=["electrical fundamentals, circuits, electronics, machines, and control concepts", "a blend of power and electronic systems rather than only one side", "applied engineering that can map into industrial, embedded, and system roles"],
        problems_and_work=["working on control panels, automation, electrical systems, and electronics-linked equipment", "supporting industrial, embedded, or operations-heavy engineering systems", "bridging hardware layers that involve both electrical and electronic behavior"],
        roles=["EEE engineer", "control and automation engineer", "industrial electronics engineer", "systems or plant engineer"],
        tradeoffs=["the branch name overlap confuses students constantly", "outcomes depend a lot on what electives, projects, and internships you choose", "it can be broad in a good way or fuzzy in a bad way if you drift"],
        good_fit_checklist=["I want both electrical and electronics exposure", "I do not need an ultra-pure branch identity", "I like systems that touch the physical world", "I am willing to shape my path actively"],
        similar_branches=["Electrical Engineering", "Electronics and Communication Engineering", "Instrumentation Engineering"],
    ),
    CourseExplainer(
        name="Information Technology",
        slug="information-technology",
        family="computing",
        overview="Focus on software systems, applications, databases, networking, and enterprise-oriented computing work.",
        who_this_fits="students who want computing careers similar to CSE, often with a slightly more applied and software-systems flavor",
        eli10="You learn how to build and manage software systems that help people and companies store information, run apps, and keep digital systems working.",
        what_you_study=["programming, databases, networking, web systems, and software engineering", "practical computing topics that support application and enterprise software work", "many overlapping concepts with CSE, depending on the college curriculum"],
        problems_and_work=["building business software, web systems, and data-backed applications", "working on databases, APIs, internal tools, and product engineering", "solving practical software problems in organizations and digital products"],
        roles=["software engineer", "web or backend engineer", "data systems engineer", "application engineer"],
        tradeoffs=["some students obsess over CSE vs IT label differences too much", "actual outcomes often depend more on college quality and your project work", "it still requires real coding skill — no free lunch, sadly"],
        good_fit_checklist=["I want software roles", "I am comfortable with coding-heavy learning", "I care more about work fit than prestige hair-splitting", "I want broad practical computing options"],
        similar_branches=["Computer Science and Engineering", "Mathematics and Computing", "Electronics and Communication Engineering"],
    ),
    CourseExplainer(
        name="Bio Technology",
        slug="bio-technology",
        family="bio",
        overview="Combine biology with engineering methods for health, industrial biology, and life-science-driven problem solving.",
        who_this_fits="students who genuinely like biology and want technical, applied, or research-linked career paths",
        eli10="You use engineering ideas to work with living systems — like cells, biological processes, and biotech tools that help health and industry.",
        what_you_study=["molecular biology, bio-process concepts, genetics-linked topics, and engineering applications", "how biological systems can be analyzed, manipulated, or used in real products and processes", "lab-heavy and science-heavy foundations compared with many traditional branches"],
        problems_and_work=["working on biotech products, biological processes, diagnostics, or applied life-science systems", "supporting R&D, lab, product, or process work in biotech-linked environments", "building foundations for higher studies in biotech, bioengineering, or related areas"],
        roles=["biotech engineer", "R&D or lab-focused roles", "process roles in biotech or pharma contexts", "higher-study-oriented technical pathways"],
        tradeoffs=["higher studies can matter a lot more here than in some mainstream branches", "students who do not actually like biology often regret the branch", "career paths can be less obvious than plug-and-play software routes"],
        good_fit_checklist=["I actually enjoy biology", "I am open to labs, research, or higher studies", "I want science-heavy engineering", "I do not need the most mainstream branch narrative"],
        similar_branches=["Biomedical Engineering", "Chemical Engineering", "Engineering Physics"],
    ),
    CourseExplainer(
        name="Mathematics and Computing",
        slug="mathematics-and-computing",
        family="computing",
        overview="Blend serious mathematics with computing, algorithms, modeling, and quantitatively demanding software problems.",
        who_this_fits="students who enjoy abstract math, algorithms, and analytical computing more than generic software hype",
        eli10="It is like taking the most math-heavy parts of computing and using them to solve harder software, data, and modeling problems.",
        what_you_study=["discrete math, probability, optimization, proofs, algorithms, and programming", "mathematical reasoning that supports advanced computing and analytical systems", "a more quantitative flavor than generic software branches"],
        problems_and_work=["algorithm-heavy software work and mathematically demanding systems", "optimization, analytics, and quantitative computing problems", "research-like or depth-heavy computing paths where math really matters"],
        roles=["software engineer", "ML or data engineer", "quantitative computing roles", "research-oriented technical roles"],
        tradeoffs=["the math load is very real", "students who choose it only for prestige can get wrecked by the abstraction", "it is excellent for the right student and miserable for the wrong one"],
        good_fit_checklist=["I truly like math", "I enjoy abstraction and analytical thinking", "I want computing with more quantitative depth", "I am okay trading some comfort for stronger intellectual fit"],
        similar_branches=["Computer Science and Engineering", "Information Technology", "Engineering Physics"],
    ),
    CourseExplainer(
        name="Engineering Physics",
        slug="engineering-physics",
        family="advanced",
        overview="Use physics-heavy foundations for engineering systems, devices, instrumentation, and analytical technical work.",
        who_this_fits="students who genuinely enjoy physics and want engineering applications, not just mainstream branch labels",
        eli10="You use serious physics to understand and build real systems and devices — not just to suffer through textbook derivations for sport.",
        what_you_study=["physics-heavy engineering foundations, mathematical modeling, and applied scientific systems", "devices, instrumentation, and analytical problem solving with stronger theory depth", "a base for specialized engineering, R&D, and higher-study-driven technical work"],
        problems_and_work=["physics-heavy engineering problems where modeling and analytical depth matter", "instrumentation, devices, specialized systems, and technical research paths", "building strong foundations for advanced engineering roles or higher studies"],
        roles=["R&D engineer", "instrumentation or device-focused engineer", "specialized technical roles", "higher-study-oriented engineering paths"],
        tradeoffs=["the branch is often misunderstood by label-chasing students", "it rewards curiosity and analytical stamina more than trend-following", "higher studies can amplify outcomes significantly here"],
        good_fit_checklist=["I genuinely enjoy physics-heavy thinking", "I can handle abstract concepts without panicking", "I am open to specialized or research-leaning paths", "I care about fit more than mainstream branch hype"],
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
