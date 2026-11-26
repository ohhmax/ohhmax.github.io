#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone generator and validator for the complete MaxHive Robot Captions Dataset.
Includes all 50 existing triggers + 35 new interactive click, skill, project, and prank triggers.
Strict criteria:
- Min 8 captions per language (in & en)
- Max 1-2 emojis per caption
- Max 12 words per caption
- Zero em-dashes and zero en-dashes
"""

import json
import os
import re
import sys

# Ensure repository root is in sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import tools.build_robot_captions as brc

CAPTIONS = dict(brc.CAPTIONS_DATA)

# NEW INTERACTIVE & CLICK TRIGGERS
NEW_TRIGGERS = {
    "skill_python": {
        "in": [
            "Python: Automation se AI tak, Max ka script bulletproof hai 🐍",
            "Clean indentation aur readable code: Python me Max master hai 💻",
            "Pandas, NumPy, scripts: Data handling ekdum butter smooth hai ⚡",
            "Python scripts background me run hoti hain, zero lag ke sath 🚀",
            "Asyncio aur Fast API: Max ke Python builds scale karte hain 🛠️",
            "Boring tasks automate karne ho? Max ka Python script bulao 🤖",
            "Python lover spotted! Chalo milke clean pipelines banate hain 🤝",
            "Script chal gayi boss! Python me bugs ka naam-o-nishan nahi ✨"
        ],
        "en": [
            "Python power: From AI tooling to automation, Max writes clean code 🐍",
            "Clean syntax and high performance: Python scripts engineered to perfection 💻",
            "FastAPI and data pipelines: Scalable backend engineering at its finest ⚡",
            "Automating complex workflows effortlessly with robust Python scripts 🚀",
            "Need rock-solid async services? Python architecture built right here 🛠️",
            "Python enthusiast detected! Let's build scalable pipelines together 🤝",
            "Zero spaghetti code: Pure pythonic elegance and modular architecture ✨",
            "High-performance Python engineering tailored for production scale 🤖"
        ]
    },

    "skill_javascript": {
        "in": [
            "Vanilla JavaScript: Zero framework bloat, 100% fast performance ⚡",
            "Event loop aur async await: JS me Max ka flow solid 🚀",
            "DOM manipulation itni fast hai ki 60 FPS guaranteed hai 💨",
            "Heavy frameworks ke bina bhi aisi smooth UI banti hai 🎨",
            "Console.log kam, clean production code zyada likhte hain hum 💻",
            "JavaScript runtime master: Har browser me butter smooth chalta hai ✨",
            "Callbacks aur Promises: Asynchronous code me koi confusion nahi 🧠",
            "Modern ES6+ syntax ke sath vanilla JS power dekh lo 😉"
        ],
        "en": [
            "Vanilla JavaScript: Zero framework bloat, pure 60 FPS speed ⚡",
            "Mastering event loops and asynchronous workflows with precision 🚀",
            "Lightweight DOM manipulation engineered for blazing fast rendering 💨",
            "Clean ES6+ architecture delivering reactive interfaces effortlessly 🎨",
            "Fewer console logs, more enterprise-grade production code 💻",
            "JavaScript runtime mastery: Flawless execution across every modern browser ✨",
            "Promises and async patterns architected for high reliability 🧠",
            "Pure vanilla speed: Demonstrating what lightweight code can achieve 😉"
        ]
    },

    "skill_typescript": {
        "in": [
            "TypeScript: Strong types aur zero runtime surprises, pure peace 🛡️",
            "Strict type safety se production bugs pehle hi pakde jate hain 🔍",
            "Generics aur Interfaces: Code architecture ekdum solid banta hai 📐",
            "Compile time pe bug pakadna: TypeScript ka yahi to maza hai 💡",
            "Type safety pasand hai? Tum aur Max pakke dost banoge 🤝",
            "Refactoring me zero darr, kyunki TypeScript sath khada hai 🚀",
            "Complex data structures bhi type-safe rehte hain hamesha ✨",
            "TypeScript code review me 10/10 marks milte hain boss 📝"
        ],
        "en": [
            "TypeScript: Strong typing and zero runtime surprises, pure peace 🛡️",
            "Catching bugs at compile time with rigorous type safety 🔍",
            "Generics and interfaces engineered for enterprise software architecture 📐",
            "Refactor fearlessly with comprehensive type definitions in place 💡",
            "Love type safety? You and Max will collaborate seamlessly 🤝",
            "Eliminating entire classes of runtime errors through strict typing 🚀",
            "Complex domain models kept clean, readable, and predictable ✨",
            "Enterprise-grade TypeScript that sails through code reviews effortlessly 📝"
        ]
    },

    "skill_c_cpp": {
        "in": [
            "C and C++: Direct memory control aur hardware level performance ⚡",
            "Pointers aur memory allocation: Yaha har byte bachta hai 🧠",
            "Embedded systems aur microcontrollers me C++ ka koi tod nahi 🔌",
            "Zero abstraction cost: Maximum raw processing power unlock hoti hai 🚀",
            "Segfault nahi aane denge, clean memory management meri pehchan hai 🛡️",
            "Operating systems se robotics tak, C++ me sab fit hai 🤖",
            "Low level hardware coding me Max ka hath ekdum pakka hai 🛠️",
            "Hardware control pasand hai? C++ code inspection kar lo ✨"
        ],
        "en": [
            "C and C++: Direct memory control and raw speed ⚡",
            "Precision pointer arithmetic and zero-overhead memory allocation 🧠",
            "Embedded microcontrollers and native hardware driven by modern C++ 🔌",
            "Zero abstraction overhead: Unlocking maximum hardware performance 🚀",
            "Robust memory hygiene and deterministic execution every single cycle 🛡️",
            "From kernel drivers to robotics, C++ drives core systems 🤖",
            "Low-level systems expertise delivering predictable native throughput 🛠️",
            "Reviewing native systems? Check out the C++ firmware modules ✨"
        ]
    },

    "skill_linux": {
        "in": [
            "Linux kernel aur Bash: Terminal me hi hamara asli ghar hai 🐧",
            "Root permission granted! Kernel level respect for fellow Linux lovers 💻",
            "sudo permissions ke sath system control ekdum seamless rehta hai ⚡",
            "Arch Linux aur Debian setups: Custom configs me Max pro hai 💻",
            "Cron jobs, systemd, aur shell scripts: Automation chalti rehti hai 🚀",
            "GUI se zyada maza terminal commands run karne me aata hai 🖤",
            "Server monitoring aur system telemetry: Linux pe command tight hai 📡",
            "Terminal power user ho? Linux geeks ke sath vibe match hoti 🤝"
        ],
        "en": [
            "Linux kernel and Bash: The terminal is our natural home 🐧",
            "Root access and systems administration handled with total precision ⚡",
            "Arch Linux and Debian environments customized for ultimate productivity 💻",
            "Automating system pipelines with shell scripts and systemd services 🚀",
            "Terminal efficiency: Where true engineering control happens 🖤",
            "Live server monitoring and Linux telemetry configured to scale 📡",
            "Keyboard-driven development using advanced terminal workflows ⌨️",
            "Linux power user? You'll appreciate the low-level systems craft 🤝"
        ]
    },

    "skill_docker": {
        "in": [
            "Docker: 'Mera laptop pe chal raha tha' wali dikkat khatam 🐳",
            "Multi-stage builds se image size super chhota ho jata hai 📦",
            "Containers deploy karo aur production me shanti se so jao 🚢",
            "Docker compose se poora stack ek second me live hota hai ⚡",
            "Isolated environments: Dependencies ka jhamela zero ho jata hai 🛠️",
            "Dev to prod parity: Har server pe identical behavior milta hai 🚀",
            "Container orchestration pasand hai? Docker setups check kar lo 🌐",
            "Lightweight images aur fast startup: Production deployment ready hai ✨"
        ],
        "en": [
            "Docker: Eliminating 'it works on my machine' forever 🐳",
            "Multi-stage builds engineered for minimal container image footprints 📦",
            "Deploy immutable containers and sleep soundly on release days 🚢",
            "Full stack orchestration spin up in seconds via Docker Compose ⚡",
            "Isolated environments eliminating dependency friction across all teams 🛠️",
            "True dev-to-production parity guaranteed across every server 🚀",
            "Love containerization? Inspect our modular Docker compose definitions 🌐",
            "Fast startups, lightweight footprints, and resilient microservices ready ✨"
        ]
    },

    "skill_react": {
        "in": [
            "React: Component architecture aur re-usable UI blocks ka jadu ⚛️",
            "Custom hooks aur memoization: Unnecessary re-renders zero rehte hain ⚡",
            "State management clean ho to complex dashboards bhi smooth lagte hain 📱",
            "Interactive frontend experiences jo users ko baandh ke rakhti hain ✨",
            "React ecosystems me clean modular code likhna Max ki aadat hai 💡",
            "Props drilling khatam: Context aur modular store use karte hain 🚀",
            "Virtual DOM optimization se UI ekdum fluid render hoti hai 💨",
            "React components crafted with high polish and zero bloat 🎨"
        ],
        "en": [
            "React: Component-driven architecture built for reuse and clarity ⚛️",
            "Custom hooks and memoization preventing wasteful re-renders ⚡",
            "Clean state management keeping complex web applications responsive 📱",
            "Interactive interfaces engineered to keep users engaged and delighted ✨",
            "Architecting maintainable frontend ecosystems with modern best practices 💡",
            "Clean data flow: Context APIs and state stores well organized 🚀",
            "Optimized virtual DOM reconciliation delivering butter-smooth 60 FPS 💨",
            "Pixel-perfect React component hierarchies built for scalable growth 🎨"
        ]
    },

    "skill_node": {
        "in": [
            "Node.js: Non-blocking I/O aur high concurrency backend power 🟢",
            "REST APIs aur microservices: Fast throughput ke sath handle hoti hain ⚡",
            "Event-driven architecture: Thousands of concurrent requests smooth chalti hain 🚀",
            "Express aur Fastify: Lightweight server pipelines bina overhead ke 🛠️",
            "Database connections pool karke ultra-low latency milti hai 💾",
            "Full-stack JavaScript: Frontend aur backend ek hi language me synced 🤝",
            "Production monitoring aur error handling: Crash-proof servers bante hain 🛡️",
            "Backend speed matters! Node.js APIs instantly response deti hain 💨"
        ],
        "en": [
            "Node.js: Non-blocking I/O and high concurrency backend power 🟢",
            "High-throughput REST APIs and microservices serving fast requests ⚡",
            "Event-driven architecture handling thousands of concurrent connections 🚀",
            "Lightweight HTTP services configured without unnecessary bloat 🛠️",
            "Optimized connection pooling delivering sub-millisecond query responses 💾",
            "Full-stack cohesion: Seamless TypeScript across client and server 🤝",
            "Resilient error boundaries and production monitoring keeping servers online 🛡️",
            "Backend performance engineered for immediate response times 💨"
        ]
    },

    "skill_arduino": {
        "in": [
            "Arduino aur ESP32: Real world electronics ko code se nachana 🔌",
            "Sensors, relays, aur motors: Physical computing ka asli maza yahi hai 🤖",
            "Wi-Fi aur Bluetooth BLE: Wireless hardware automation 100% working 📡",
            "EEPROM me state save: Power cut pe bhi data safe rehta 💡",
            "Soldering se breadboard tak: Max hardware aur software dono janta hai 🛠️",
            "IoT Home Automation: Ghar ke appliances phone se control hote hain 🏠",
            "MicroPython aur C++: Microcontroller coding me zero delay magic ✨",
            "Hardware hacking pasand hai? Induction car project dekh lo boss ⚡"
        ],
        "en": [
            "Arduino and ESP32: Bridging physical hardware with embedded code 🔌",
            "Sensors, relays, and actuators: The true thrill of physical computing 🤖",
            "Wi-Fi and BLE integration driving real-time wireless telemetry 📡",
            "EEPROM persistence ensuring zero data loss during power fluctuations 💡",
            "From schematics to breadboards: Mastering both hardware and firmware 🛠️",
            "IoT Home Automation: Controlling real-world appliances with sub-second response 🏠",
            "MicroPython and native C++ driving optimized microcontroller firmware ✨",
            "Love hardware engineering? Check out our induction vehicle build ⚡"
        ]
    },

    "skill_android": {
        "in": [
            "Native Android: Java aur Kotlin me fluid apps build hoti hain 📱",
            "Background services, WorkManager, aur battery optimization me top skills ⚡",
            "Root tools, ADB commands, aur custom shell scripts ready hain 🛠️",
            "Material 3 design aur responsive layouts har screen pe chamakte hain ✨",
            "APK size lightweight rehta hai aur memory leaks zero hoti hain 🛡️",
            "Phone hardware sensors aur camera APIs direct integrate hote hain 📸",
            "Android developer spotted! Mobile innovations pe sath kaam karein 🤝",
            "Butter smooth scrolling aur zero frame drop on every device 💨"
        ],
        "en": [
            "Native Android: High-performance apps built in Kotlin and Java 📱",
            "Background WorkManager pipelines tuned for optimal battery efficiency ⚡",
            "Deep system integration via ADB, shell scripts, and system services 🛠️",
            "Material 3 interfaces adapting seamlessly to every screen size ✨",
            "Lightweight APK footprints with zero memory leaks in production 🛡️",
            "Direct hardware sensor telemetry and camera pipeline integration 📸",
            "Android engineering that delivers responsive mobile software 🤝",
            "Fluid 120Hz refresh rates and zero frame drops guaranteed 💨"
        ]
    },

    "skill_go": {
        "in": [
            "Go (Golang): Goroutines aur channels se super-fast concurrency milti hai 🐹",
            "Single static binary: Deployment me zero dependency tension hoti hai 📦",
            "Microservices itni fast banti hain ki server bills aadhe ho jayein 💰",
            "Garbage collection tuned hai, memory footprint hamesha light rehta hai ⚡",
            "Cloud native tools aur networking me Go ka koi mukabla nahi 🌐",
            "Simple, readable syntax: Bina complexity ke solid systems bante hain 🚀",
            "Golang lover ho? High performance backend discussion banta hai 🤝",
            "Compile and ship: Production reliability 100% guaranteed rehti hai ✨"
        ],
        "en": [
            "Go (Golang): Lightweight goroutines delivering effortless concurrency 🐹",
            "Single static binary output: Zero runtime dependency headaches 📦",
            "Microservices architected to cut server compute overhead in half 💰",
            "Low-latency garbage collection keeping memory footprints minimal ⚡",
            "Cloud-native networking and distributed systems built for scale 🌐",
            "Simple, pragmatic syntax producing highly reliable software 🚀",
            "Building in Go? Let's talk high-performance systems engineering 🤝",
            "Compile, test, and ship: Production grade backend reliability ✨"
        ]
    },

    "skill_git": {
        "in": [
            "Git: Clean commit history aur atomic commits likhna Max ka rule 🌳",
            "Git rebase aur merge conflicts: Bina ghabraye sab resolve hota hai 🛡️",
            "Branching strategy tight ho to team deployment smooth rehti hai 🚀",
            "GitHub repos me proper documentation aur README zaroori hota hai 📝",
            "Git cherry-pick aur stash: Power user tools me full command hai ⚡",
            "Open source contributions pasand hain? GitHub profile check karo ⭐",
            "Commit messages itne clear hain ki poori story samajh aa jaye 💡",
            "Version control master: Codebase hamesha organized rehta hai ✨"
        ],
        "en": [
            "Git: Clean commit histories and atomic changes are our standard 🌳",
            "Navigating rebases and merge conflicts with total confidence 🛡️",
            "Branching workflows architected for seamless multi-developer shipping 🚀",
            "Comprehensive documentation and structured READMEs across every repo 📝",
            "Mastering cherry-picks, stashing, and advanced Git plumbing commands ⚡",
            "Love open source? Star our repositories on GitHub ⭐",
            "Descriptive commit messages that document the architectural intent 💡",
            "Version control expertise keeping codebases pristine and trackable ✨"
        ]
    },

    "skill_generic": {
        "in": [
            "Skills dekh rahe ho? Hardware se cloud tak full spectrum hai 💻",
            "Har skill ke peeche real projects aur verified experience hai 🏆",
            "Technology badalti rehti hai, par core logic hamesha solid rehta hai 🧠",
            "MCA graduate mind: Nayi tech stack seekhne me friction zero rehta ⚡",
            "Tool choose karne me bias nahi: Right tool for right job 🛠️",
            "Problem solving aur system design: Yaha asli engineering hoti hai ✨",
            "Aisi skills company ki technical debt ko zero kar sakti hain 😉",
            "Tech stack pasand aaya? Chalo sath me bada build karte hain 🚀"
        ],
        "en": [
            "Exploring skills? From bare metal hardware to cloud deployments 💻",
            "Every skill backed by shipping projects and verified milestones 🏆",
            "Syntax changes constantly, but core problem-solving fundamentals endure 🧠",
            "Rapid learner: Mastering new stacks and toolkits without friction ⚡",
            "No language dogmatism: Always selecting the best tool for the job 🛠️",
            "System architecture and algorithm design: Where software truly shines ✨",
            "Technical versatility that eliminates organizational tech debt 😉",
            "Impressed by the stack? Let's build something extraordinary together 🚀"
        ]
    },

    "project_car": {
        "in": [
            "Wireless Induction Car: Bina battery ke magnetic flux se chalti hai! 🚗⚡",
            "Physics aur embedded coding ka kamaal: Real world hardware prototype 🔋",
            "Wireless power transfer: Track se seedha energy absorb hoti hai 🔌",
            "College project tha par engineering level pure industrial hai boss 🏆",
            "Circuit schematics se soldering tak: 100% self-made hardware build 🛠️",
            "Har koi software banata hai, Max physical hardware bhi banata hai 🤖",
            "Demonstration dekhoge to hairan reh jaoge: Zero battery weight! 🚀",
            "Future transportation concept: Clean wireless energy on wheels ✨"
        ],
        "en": [
            "Wireless Induction Car: Powered solely via magnetic flux transfer! 🚗⚡",
            "Physics meets embedded firmware: A fully functional hardware prototype 🔋",
            "Wireless energy transmission: Absorbing drive power directly from tracks 🔌",
            "From academic prototype to industrial-grade hardware execution 🏆",
            "Schematics, PCB fabrication, and soldering: 100% handcrafted build 🛠️",
            "Bridging hardware and software: Physical computing engineered right 🤖",
            "Zero battery deadweight: Demonstrating wireless energy delivery 🚀",
            "Future mobility concept: Sustainable wireless propulsion in action ✨"
        ]
    },

    "project_maxai": {
        "in": [
            "MaxAI: Local LLM runtime! Phone pe offline AI model chalta hai 🤖",
            "Zero cloud dependency: Aapka data kabhi device se bahar nahi jata 🛡️",
            "Quantized GGUF models: Android GPU aur NPU pe ultra-fast speed ⚡",
            "Internet band hone pe bhi AI calculations 100% working rehti hain 📱",
            "Cloud API bills khatam! Autonomous local intelligence ka maza lo 💡",
            "Sub-second token generation: On-device latency almost zero rehti hai 🚀",
            "Next-gen edge computing: Phone ko AI workstation bana diya Max ne ✨",
            "Privacy-first AI: Confidential prompts device ke andar hi rehte hain 🔒"
        ],
        "en": [
            "MaxAI: Local on-device LLM runtime running 100% offline 🤖",
            "Zero cloud dependence: Confidential data never leaves your device 🛡️",
            "Quantized GGUF runtimes tuned directly for mobile NPU and GPU ⚡",
            "Reliable AI inference even when offline or in airplane mode 📱",
            "Eliminating recurring cloud API fees with local neural execution 💡",
            "Sub-second token delivery: Blazing fast on-device inference speeds 🚀",
            "Next-generation edge intelligence engineered directly on mobile hardware ✨",
            "Privacy-by-design: Personal prompts stay strictly in local memory 🔒"
        ]
    },

    "project_celllock5g": {
        "in": [
            "CellLock5G: 5G band lock karke high speed internet maintain karta hai 📡",
            "n28 aur n78 bands: Slow fallback towers ko block karta hai ⚡",
            "Carrier aggregation force karke maximum download speed milti hai 🚀",
            "Real-time RSRP aur SINR telemetry: Signal strength graphs live dikhte hain 📊",
            "Telecom engineers ke liye dream tool: Radio parameters full control me 📱",
            "Call drops khatam: Stable 5G connection lock rehta hai 🛡️",
            "Qualcomm aur MediaTek radio chipsets ke sath direct interaction 📶",
            "Network optimization me Max ka engineering level pro hai boss 🏆"
        ],
        "en": [
            "CellLock5G: Locking high-speed 5G bands for uninterrupted throughput 📡",
            "Locking sub-6GHz bands (n28/n78) and blocking congested fallback towers ⚡",
            "Forced carrier aggregation unlocking maximum cellular download speeds 🚀",
            "Live RSRP and SINR telemetry visualized in real-time graphs 📊",
            "A power tool for radio optimization and cellular field diagnostics 📱",
            "Eliminating speed throttling: Keeping high-frequency 5G radios locked 🛡️",
            "Low-level radio modem integration across modern cellular chipsets 📶",
            "Telecom software engineering designed for mission-critical reliability 🏆"
        ]
    },

    "project_maxter": {
        "in": [
            "MAXTER: Android phone ko full Arch Linux workstation bana deta hai 🐧",
            "Zsh, custom aliases, aur developer tools pre-configured milte hain ⚡",
            "Termux environment me root permissions aur package management seamless hai 💻",
            "Phone se server deploy karo aur C++ code compile kar lo 🚀",
            "Mobile developer productivity: Laptop kholne ki zaroorat nahi padti 📱",
            "Clean scripts aur optimized performance: 0 lag terminal workflow 🛠️",
            "Hackers aur developers ka favorite companion: MAXTER suite 🖤",
            "Linux terminal power in your pocket: Kahi se bhi code karo ✨"
        ],
        "en": [
            "MAXTER: Transforming Android smartphones into Arch Linux workstations 🐧",
            "Pre-configured Zsh setups, developer aliases, and productivity toolchains ⚡",
            "Seamless package management and developer environments inside Termux 💻",
            "Compile C++ code and administer remote servers right from mobile 🚀",
            "True mobile engineering independence without carrying a heavy laptop 📱",
            "Streamlined scripts delivering lightweight, zero-latency terminal workflows 🛠️",
            "A beloved utility for developers, system admins, and security pros 🖤",
            "Complete Linux terminal capabilities directly inside your pocket ✨"
        ]
    },

    "project_luci": {
        "in": [
            "LuCI Cyber Theme: OpenWrt router interface ko cyberpunk look diya hai 🌐",
            "Real-time bandwidth graphs aur active DHCP clients live dikhte hain 📊",
            "Old boring router UI ko responsive dark glassmorphic dashboard banaya ⚡",
            "Phone ya tablet pe router manage karna ab super easy hai 📱",
            "Home-lab aur networking enthusiasts ke beech ye theme viral hai 🚀",
            "Pure CSS grid aur hardware-accelerated SVG meters use kiye hain 🎨",
            "Slow router processor pe bhi 60 FPS smooth animation chalti hai 💨",
            "Open source router customization: Network engineering at its coolest 🛠️"
        ],
        "en": [
            "LuCI Cyber Theme: Modern cybernetic interface for OpenWrt routers 🌐",
            "Real-time bandwidth monitoring and active DHCP device telemetry 📊",
            "Replacing dated router interfaces with responsive glassmorphic dashboards ⚡",
            "Inspecting router diagnostics seamlessly on both mobile and tablets 📱",
            "Widely adopted by home-lab builders and networking professionals 🚀",
            "Crafted with lightweight CSS grid and hardware-accelerated SVG graphs 🎨",
            "Smooth 60 FPS rendering even on low-power embedded router CPUs 💨",
            "Open-source router dashboard modernization at its best 🛠️"
        ]
    },

    "project_ipcai": {
        "in": [
            "IPCAI Studio: CCTV cameras ke liye edge AI motion alerting studio 📹",
            "Cloud subscriptions khatam: Sara video processing locally hota hai 🔒",
            "RTSP streaming aur OpenIPC discovery: Sub-second latency milti hai ⚡",
            "Local storage recording: Monthly cloud fees se hamesha ke liye aazadi 💾",
            "Computer vision se instant motion detection bina kisi false alarm ke 🎯",
            "Python backend aur fast stream ingestion: 24/7 reliability milti hai 🚀",
            "Smart surveillance system jo aapki privacy ki izzat karta hai 🛡️",
            "Security cameras ko intelligent banane ka open-source formula ✨"
        ],
        "en": [
            "IPCAI Studio: Edge AI smart vision studio for security cameras 📹",
            "Zero cloud fees: All computer vision processing happens on premises 🔒",
            "Multi-channel RTSP ingestion and automated OpenIPC hardware discovery ⚡",
            "Local recording pipelines freeing users from recurring cloud subscriptions 💾",
            "Computer vision motion segmentation filtering out false camera alerts 🎯",
            "Python streaming engine engineered for dependable 24/7 uptime 🚀",
            "Smart security surveillance engineered with privacy at its center 🛡️",
            "Transforming low-cost CCTV hardware into intelligent video appliances ✨"
        ]
    },

    "project_generic": {
        "in": [
            "Project details: Har ek line purpose ke sath likhi hai 💡",
            "Architecture aur clean code: Production me yahi kaam aata hai 📐",
            "Case studies padh ke dekho, technical depth samajh aayegi 🔍",
            "Live demo ya code dekhna ho to GitHub pe tap karo 🌐",
            "Idea se execution tak: Max projects ko end-to-end deliver karta hai 🚀",
            "Har project me real-world problem solve ki gayi hai 🎯",
            "Kaunsa project sabse mast laga? Contact form me batao mujhe 💬",
            "Hardware se scalable web apps: Variety dekh ke maza aaya na? ✨"
        ],
        "en": [
            "Reviewing project specs? Every single component serves a distinct purpose 💡",
            "Clean architecture and reliability: What truly matters in production 📐",
            "Inspect these case studies to explore the systems engineering depth 🔍",
            "Want live code or demonstrations? Click the technical documentation links 🌐",
            "From concept to deployment: Delivering end-to-end software solutions 🚀",
            "Every single project directly addresses a tangible engineering challenge 🎯",
            "Which build stood out most? Let me know in contact section 💬",
            "From embedded circuits to web apps: Diverse technical craftsmanship ✨"
        ]
    },

    "click_testimonials": {
        "in": [
            "Testimonials dekh rahe ho? Client track record hamesha 10/10 rehta ⭐",
            "Verified feedback: Har review ke peeche on-time delivery ki kahani hai 🤝",
            "Client satisfaction hi asli kamai hai! Padho aur trust karo 🏆",
            "Technical clarity aur dedication: Testimonials me log yahi bolte hain ✨",
            "Aapki company bhi 5-star review degi jab Max ko hire karoge 😉",
            "Freelance se enterprise tak: Clients hamesha khush rehte hain 💼",
            "Honest reviews: Zero fake PR, pure verified engineering impact 📜",
            "Padh liya? Review dene ke liye ab hire kar lo 🚀"
        ],
        "en": [
            "Reading testimonials? Client satisfaction track record is consistently 10/10 ⭐",
            "Verified client feedback reflecting punctual delivery and clean code 🤝",
            "Client trust is earned: Review real-world engineering endorsements 🏆",
            "Technical clarity and relentless dedication highlighted in every review ✨",
            "Your team will leave a 5-star review after hiring Max 😉",
            "From agile startups to production systems: Consistently happy collaborators 💼",
            "Honest endorsements: Zero fluff, pure verified technical impact 📜",
            "Done reading? Now let's collaborate and build your next success story 🚀"
        ]
    },

    "click_gallery": {
        "in": [
            "Moments gallery: Hardware builds aur college journeys ki photos hain 📸",
            "Engineering sirf code nahi, real-life memories aur projects bhi hain 🌟",
            "Video dekh rahe ho? Hardware live chalte dekhne ka alag maza 🎥",
            "Hackathons, labs, aur prototypes: Har photo me mehnat dikhti hai 🛠️",
            "Photos dekh ke Max ka journey samajh aata hai: Pure passion! ❤️",
            "Timeline explore karo: Student se MCA systems engineer banne ka safar 🎓",
            "Boring portfolio nahi hai ye! Real hardware moments live capture hain ✨",
            "Full screen me photo dekhi? Har angle se engineering clean hai 🔍"
        ],
        "en": [
            "Moments gallery: Behind-the-scenes snapshots of hardware and prototypes 📸",
            "Engineering is more than syntax: Capturing hands-on builds and milestones 🌟",
            "Watching demo footage? Nothing beats seeing physical hardware in motion 🎥",
            "Hackathons, university labs, and prototypes: Passion in every frame 🛠️",
            "Exploring the gallery reveals Max's journey and dedication to tech ❤️",
            "Browse the visual timeline from early prototypes to MCA systems engineering 🎓",
            "A dynamic portfolio showcasing verified real-world engineering moments ✨",
            "Full-screen view active: Inspecting technical milestones up close 🔍"
        ]
    },

    "click_contact_github": {
        "in": [
            "GitHub link pe click kiya? Repositories me star dena mat bhoolna ⭐",
            "Open source repos open: Commits aur clean code inspect kar lo 💻",
            "GitHub profile pe saare projects ka source code transparently rakha hai 🔍",
            "Follow button daba do, naye tools launch hone pe notification aayega 🔔",
            "Clean git history aur verified commits dekh ke dil khush hoga ✨",
            "GitHub pe explore karo, bahut saare useful utilities milenge aapko 🛠️",
            "Code speaks louder than words: GitHub inspect karke verify kar lo 🚀",
            "Star de diya kya? AI robot ki taraf se thanks dost 💙"
        ],
        "en": [
            "Checking GitHub? Drop a star on the open source repositories ⭐",
            "Open repositories available: Inspect commit discipline and source code 💻",
            "Transparent open source software hosted publicly on GitHub 🔍",
            "Hit follow to stay updated as new developer tools are released 🔔",
            "Pristine commit hygiene and verified commits ready for inspection ✨",
            "Explore our GitHub profile for standalone utilities and developer suites 🛠️",
            "Code speaks louder than words: Audit our repos directly on GitHub 🚀",
            "Dropped a star? Much appreciation from your AI robot companion 💙"
        ]
    },

    "click_contact_linkedin": {
        "in": [
            "LinkedIn pe connect ho rahe ho? Connection request accept ho jayegi 🤝",
            "Professional network pe welcome! DM me role details discuss kar lo 💼",
            "LinkedIn message bhej do: Quick response guaranteed rehta hai 📨",
            "Network banana acchi baat hai! Let's connect on LinkedIn 🌐",
            "Recommendations aur verified skills check kar lo LinkedIn profile pe ⭐",
            "Career timeline aur engineering impact: LinkedIn pe full record hai 📜",
            "Direct message open hai! Technical partnership discuss karein 🚀",
            "Connection sent? Chalo professional dosti pakki hui boss 🤝"
        ],
        "en": [
            "Connecting on LinkedIn? Great idea, invitations are reviewed promptly 🤝",
            "Welcome to our professional network! Let's discuss open opportunities 💼",
            "Send a direct message on LinkedIn for rapid technical discussions 📨",
            "Expanding professional networks: Glad to connect with engineering peers 🌐",
            "Review verified endorsements and technical impact on our LinkedIn profile ⭐",
            "Comprehensive career timeline and technical milestones documented on LinkedIn 📜",
            "Direct messages open: Reach out to discuss architectural partnerships 🚀",
            "Connection request sent? Looking forward to staying in touch 🤝"
        ]
    },

    "click_contact_telegram": {
        "in": [
            "Telegram pe ping? Instant reply milne ke chances 100% hain ✈️",
            "Fast messaging channel: Direct conversation shuru karne ke liye best hai 💬",
            "Telegram channel pe active rehte hain, bindaas 'Hi' bol do 📱",
            "Instant messaging speed: Telegram pe deal jaldi pack hoti hai 🚀",
            "Quick queries ya quick feedback? Telegram pe instant connectivity milti hai ⚡",
            "Fast communication line open! Type karke send daba do boss 📨",
            "Bina delay baat karni ho to Telegram number 1 choice hai 🌐",
            "Telegram DM received? Max seconds me reply karta hai dost ⏱️"
        ],
        "en": [
            "Messaging on Telegram? Fastest route for immediate technical responses ✈️",
            "Direct messaging channel: Perfect for rapid, informal project discussions 💬",
            "Active on Telegram daily: Feel free to say hello anytime 📱",
            "Real-time communication: Fast alignment on upcoming technical roles 🚀",
            "Quick questions or immediate feedback? Telegram offers direct low-latency chats ⚡",
            "Direct line open: Send over project outlines on Telegram today 📨",
            "Zero communication delays: Telegram is our fastest messaging channel 🌐",
            "Got a quick message? Telegram chats get reviewed within minutes ⏱️"
        ]
    },

    "click_contact_email": {
        "in": [
            "Email pe click kiya? Offer letter draft karna shuru kar do 📧",
            "Direct inbox ping! Subject line me 'Job Offer' likhna ✉️",
            "Email notifications active hain: 2 ghante me response mil jayega 📬",
            "Professional enquiry ke liye email hamesha best option hota hai 💼",
            "Job specs ya project scope email pe direct share kar lo 📄",
            "Clean inbox etiquette: Har email ka fast professional reply milta ✍️",
            "Formal email bhejo! Inbox aapke message ka wait kar raha hai 📨",
            "Email draft ready? Send daba do, hum wait kar rahe hain 🚀"
        ],
        "en": [
            "Opening email? Time to draft that official offer letter 📧",
            "Direct inbox delivery: Feel free to share project specifications ✉️",
            "Email notifications active: Expect a thoughtful technical response promptly 📬",
            "Email remains the best channel for detailed architectural proposals 💼",
            "Send over technical specifications or team roles directly via email 📄",
            "Punctual inbox habits: All technical inquiries answered with high clarity ✍️",
            "Let's initiate formal discussions: Inbox is ready for your proposal 📨",
            "Draft complete? Hit send and let's get building together 🚀"
        ]
    },

    "click_contact_phone": {
        "in": [
            "Phone dialer open! Direct call karke deal fix kar lo 📞",
            "Direct voice call: Fast communication aur quick alignment ke liye best 📱",
            "Phone pe baat karke dekho, technical problems ka instant solution milega 🗣️",
            "Phone number save kar lo, urgent project requirements me kaam aayega 📲",
            "Quick phone screen? Max technical discussion ke liye hamesha ready hai 🤝",
            "Voice communication se clarity milti hai: Direct call kar lo dost 💬",
            "Number dialed! Technical requirements seedha phone pe discuss karein ☎️",
            "Direct mobile contact: No agents, no middlemen, direct developer connection 🚀"
        ],
        "en": [
            "Opening phone dialer? Call directly to discuss upcoming engineering needs 📞",
            "Direct voice line: Fastest way to align on technical expectations 📱",
            "Discuss systems architecture and engineering roles directly over a call 🗣️",
            "Save the contact info for urgent engineering sprints and advice 📲",
            "Ready for a technical phone screen? Max is always prepared 🤝",
            "Voice conversations build immediate clarity: Feel free to ring directly 💬",
            "Number dialed! Let's talk system requirements directly over phone ☎️",
            "Direct developer line: No intermediaries, pure technical communication 🚀"
        ]
    },

    "click_avatar": {
        "in": [
            "Max ki profile photo dekh rahe ho? MCA graduate, full-stack engineer 📸",
            "Photo me serious dikhta hai, par banda friendly aur humble hai 😄",
            "Professional coder look: Din me system architect, raat ko hardware builder 🌙",
            "Profile picture 10/10 na? Ab resume bhi dekh hi lo dost 📄",
            "Face of engineer: Har project ke peeche inhi ka dimaag hai 🧠",
            "Focused look! Code review ho ya deploy, attention hamesha 100% 🎯",
            "Profile photo dekhi? Real developer, real passion, verified credentials 🏆",
            "Banda smart hai aur code aur bhi zyada smart likhta hai 😎"
        ],
        "en": [
            "Admiring Max's profile? Systems engineer, MCA graduate, and innovator 📸",
            "Looks focused in photos, but incredibly collaborative and friendly in person 😄",
            "Face behind code: Architect by day, embedded builder by night 🌙",
            "Solid profile! Make sure to review the verified resume timeline too 📄",
            "Meet the engineer behind every architecture and circuit in this catalog 🧠",
            "Laser focus: From architecture design to production deployments 🎯",
            "Verified credentials, university honors, and hands-on systems impact 🏆",
            "Talented engineer who writes even smarter code for scalable systems 😎"
        ]
    },

    "click_blank_page": {
        "in": [
            "Khali jagah pe tap? Mujhe dhoondh rahe the kya? 😉",
            "Screen test chal raha hai kya? Responsive canvas 10/10 hai boss ✨",
            "Chalo ek secret prank dikhata hu! Interactive questions try karo 🕹️",
            "Kahi bhi click karo, mera AI radar har movement notice karta 🤖",
            "Bored ho rahe ho kya? Chalo ek funny joke sunata hu 😜",
            "Scroll karne ka aalas aa raha hai? Navigation dock use karo 🧭",
            "Blank click detected: AI companion aapke har step pe sath hai 🐾",
            "Cursor dance kar raha hai! Chalo main bhi dance karta hu 💃"
        ],
        "en": [
            "Tapping empty space? Looking for your friendly AI companion? 😉",
            "Display responsiveness check? The glass layout adapts cleanly to every tap ✨",
            "Care for a fun interactive prank? Check out the interactive prompts 🕹️",
            "Tap anywhere! My cybernetic sensor array tracks every movement 🤖",
            "Taking a brief pause? Let me share an insider engineering joke 😜",
            "Tired of scrolling? Use the bottom navigation deck for instant jumps 🧭",
            "Click detected: AI mascot companion is always here to guide you 🐾",
            "Cursor dancing on screen? Let me bust out a happy dance 💃"
        ]
    },

    "prank_hire_prompt": {
        "in": [
            "Max ko hire karoge ya main rone lagu? 🥺",
            "Aapki tech team me Max ke liye jagah hai na? 💼",
            "Offer letter taiyar kar rahe ho ya thoda aur inspire karun? 📜",
            "Ek honest sawal: Max ko hire karna chahte ho? 🤝",
            "Kya Max aapki dream team ka hissa banne wala hai? 🚀",
            "Interview schedule karein ya seedha signing bonus doge? 😏",
            "Aapki company ko 10x developer chahiye na? Haan bolo! ⚡",
            "Dil pe hath rakh ke bolo, portfolio 10/10 laga na? 🌟"
        ],
        "en": [
            "Will you hire Max or should I start crying? 🥺",
            "Does your tech team have an open seat for Max? 💼",
            "Drafting an offer letter or do you need more case studies? 📜",
            "Honest question: Ready to add Max to your engineering team? 🤝",
            "Is Max destined to join your high-performance tech squad? 🚀",
            "Shall we book an interview or jump straight to contract signing? 😏",
            "Your engineering team needs a 10x problem solver, right? ⚡",
            "Speaking honestly, this portfolio is an easy 10/10, isn't it? 🌟"
        ]
    },

    "prank_hire_yes": {
        "in": [
            "Yaaay! Contact form khol diya, jaldi offer letter bhej do! 🎉💃",
            "Party mode on! Engineering dream team banne wali hai 🍾🚀",
            "Best decision ever! Max team me aake aag laga dega ⚡",
            "Shukriya! Celebration dance shuru ho chuka hai robot ka 🕺✨",
            "Dil jeet liya aapne! Chalo ab technical details finalize karein 🤝",
            "Offer letter ka wait hai! Inbox hamesha open rehta hai 📧",
            "Congratulations! Aapne ek dedicated MCA engineer ko choose kiya 🎓",
            "Music lagao! Aaj to celebration night ban gayi boss 🎶"
        ],
        "en": [
            "Yaaay! Contact deck unlocked, send over that offer letter! 🎉💃",
            "Party mode engaged! An engineering dream team in the making 🍾🚀",
            "Best decision of the week! Max will accelerate your roadmap ⚡",
            "Huge appreciation! Mascot victory dance is officially in motion 🕺✨",
            "You made the right call! Let's finalize the technical specs 🤝",
            "Offer letter ready? Our inbox is standing by for details 📧",
            "Congratulations! You just secured an exceptional systems engineer 🎓",
            "Cue the celebration music! An exciting new partnership begins 🎶"
        ]
    },

    "prank_hire_no": {
        "in": [
            "Aisa mat bolo yaar! Dil ke tukde-tukde ho gaye 💔😭",
            "Error 404: Rejection not supported by friendly robot 🤖❌",
            "Aankhon se digital aansu behne lage! Soch lo ek baar aur 🥺",
            "Kyu bhai kyu? Itna clean portfolio dekh ke bhi 'No'? 😢",
            "Mera mood off ho gaya! Par main umeed nahi chhodunga 💔",
            "Thoda aur ghoom lo portfolio me, dil zaroor badal jayega 🧭",
            "Dil tod diya aapne! Par chalo dosti to bani rahegi na? 🥺",
            "Tear drop mode active: Phir bhi main aapko pasand karta hu 💧"
        ],
        "en": [
            "Don't say that! You've broken my digital heart into pieces 💔😭",
            "Error 404: Rejection protocol not found on this robot 🤖❌",
            "Digital tears streaming down! Take another look at case studies 🥺",
            "Saying no after seeing all this clean code? Heartbreaking 😢",
            "My mood subroutines are bruised, but my optimism remains strong 💔",
            "Explore the projects once more; your decision might change 🧭",
            "Heartbroken! But can we at least remain connected as tech friends? 🥺",
            "Crying active: Even so, I think you're an awesome visitor 💧"
        ]
    },

    "prank_secret_prompt": {
        "in": [
            "Ek top-secret prank dekhna hai kya? 🤫",
            "Chalo ek secret easter egg prank dikhaun aapko? 🕹️",
            "Himmat hai to 'Haan' daba ke dekho, darr mat jana! 😈",
            "Robot ka ek secret trick dekhoge? Maza aayega pakka 🎩",
            "Secret developer prank test karein? 2 second lagenge ⏱️",
            "Ek mysterious button dabaoge mere sath? [Risk included] ⚠️",
            "Code me ek hidden surprise chhupa hai, dekhna hai? 🎁",
            "Warning: Ye secret dekh ke aapki hansi chhoot sakti hai 😂"
        ],
        "en": [
            "Want to see a top-secret developer prank? 🤫",
            "Care to unlock a secret easter egg prank right now? 🕹️",
            "Hit yes if you dare; prepare to be mildly surprised! 😈",
            "Care to witness an insider robot party trick? Guaranteed fun 🎩",
            "Testing a secret developer prank? Takes only two seconds ⏱️",
            "Care to push a mysterious button with me? High curiosity! ⚠️",
            "A hidden surprise is tucked away inside this codebase, curious? 🎁",
            "Warning: Unlocking this secret might trigger sudden laughter 😂"
        ]
    },

    "prank_secret_yes": {
        "in": [
            "Bwahaha! Prank ye hai: Code me ek bhi bug nahi mila 😂",
            "Gotcha! Aapko laga crash hoga? Mera code rock solid hai boss 🛡️",
            "Pranked! Sirf aapki smile dekhne ke liye ye drama kiya tha 😄",
            "Haha! Darr gaye the na? Max code 100% bug-free rehta ✨",
            "Smile aayi na? Yahi to mera asli secret weapon hai 😉",
            "Prank success! Ab to smile ke badle contract sign karna padega 📝",
            "Haha! Virus nahi, sirf pure friendly robot love mila aapko ❤️",
            "Mission accomplished! User ke chehre pe hassi la di maine 🚀"
        ],
        "en": [
            "Bwahaha! The prank is that my code has zero bugs! 😂",
            "Gotcha! Thought it would crash? This architecture is rock solid 🛡️",
            "Pranked! Crafted that suspense to put a smile on your face 😄",
            "Haha! Mild heart attack? Don't worry, 100% bug-free code here ✨",
            "That brought a smile, didn't it? That's my true secret weapon 😉",
            "Prank successful! That smile earns an official interview invite 📝",
            "Haha! No malware here, only friendly AI companion charm ❤️",
            "Mission accomplished! Successfully delivered a cheerful laugh today 🚀"
        ]
    },

    "prank_secret_no": {
        "in": [
            "Darr gaye na? Safe coding hi hamesha achhi hoti hai 😎",
            "Fattu bolu ya sensible? Safe rehna bhi ek skill hai boss 🛡️",
            "Rejection accepted! Mystery mystery hi bani rahe to behtar hai 🕵️",
            "Risk nahi lena? Production engineers ki yahi to aadat hoti hai 📐",
            "Smart move! Bina code review ke unknown buttons nahi dabane chahiye 💡",
            "Chalo secret safe hai! Baad me himmat ho to batana 🔒",
            "Safe choice! Code me zero risks lena sabse badiya hota hai ⚡",
            "Smug robot nods: Caution is the mark of a veteran engineer 🤝"
        ],
        "en": [
            "Scared? No worries, safe defensive coding is best anyway 😎",
            "Sensible caution! Defensive engineering is an invaluable skill 🛡️",
            "Rejection accepted! Some mysteries are best left unexplored 🕵️",
            "Risk-averse? That's the signature trait of a veteran systems architect 📐",
            "Smart decision! Never push untrusted buttons without code reviews 💡",
            "The secret remains locked away! Let me know if curiosity returns 🔒",
            "Zero risk approach: Exactly what enterprise production systems demand ⚡",
            "Smug robot approval: Caution is the mark of an experienced leader 🤝"
        ]
    },

    "prank_chai_prompt": {
        "in": [
            "Chai pioge mere sath ya coffee? ☕",
            "Coding ke liye kya pasand hai: Kadak Chai ya Coffee? 🫖",
            "Ek quick developer question: Chai lover ho ya Coffee lover? ☕",
            "Chai break ka time ho gaya! Aapki choice kya hai dost? 🍪",
            "Chai ya Coffee: Is faisle pe hamari dosti depend karti hai 😉",
            "Fuel for coding: Kaunsa drink aapka dimaag fast chalata hai? ⚡",
            "Garma garam chai bhejoon ya cold brew coffee? Batao jaldi ☕",
            "Tension mat lo, dono drinks bug fix me help karti 💡"
        ],
        "en": [
            "Cup of tea with me or coffee? ☕",
            "What fuels your coding sessions: Rich Tea or Strong Coffee? 🫖",
            "Vital developer question: Are you Team Tea or Team Coffee? ☕",
            "Mid-day beverage break! What's your drink of choice today? 🍪",
            "Tea versus Coffee: Our developer friendship hinges on this choice 😉",
            "Fueling late night builds: Which beverage keeps your focus sharp? ⚡",
            "Steaming hot tea or chilled iced coffee? Cast your vote now ☕",
            "No worries either way, both drinks are proven bug-fixing fuels 💡"
        ]
    },

    "prank_chai_yes": {
        "in": [
            "Ekdum sahi choice dost! Chai aur coding ka combo unbeatable hai 🫖✨",
            "Chai supremacy zindabad! Adrak aur elaichi wali chai best hai ☕",
            "Dil khush kar diya! Sacha Indian coder chai pe chalta hai 🇮🇳❤️",
            "Chai piyo, bug bhagao! Ab to hamari dosti pakki ho gayi 🤝",
            "Chai ki yaad dila di! Ab interview chai pe hoga ☕",
            "Parle-G biscuit bhi sath me rakh lo, coding session set hai 🍪",
            "Chai lover spotted: Mere algorithms bhi chai sunke fast chalte hain ⚡",
            "Shandar choice! Warm tea aur high-performance code ka joda mast hai ✨"
        ],
        "en": [
            "Top choice! Tea and clean code make an unbeatable match 🫖✨",
            "Tea supremacy confirmed! A warm brew powers the sharpest logic ☕",
            "Excellent taste! Classic tea keeps developer spirits resilient and calm 🫖❤️",
            "Sip tea, crush bugs: Collaboration is off to a great start 🤝",
            "Kettle boiled and tea poured! Best fuel for architectural deep work ☕",
            "Grab a biscuit, and let's ship solid code together 🍪",
            "Tea connoisseur detected: My algorithms hum faster with tea around ⚡",
            "Splendid choice! High-performance systems paired with fine tea ✨"
        ]
    },

    "prank_chai_no": {
        "in": [
            "Traitor! Coffee bhi chalegi jab tak code fast run kare ☕😜",
            "Coffee lover spotted! Caffeine overdose se production crash mat kar dena 😂",
            "Chai reject ki? Thoda dukh hua, par coffee bhi respectable hai ☕",
            "American style coder lagte ho! Espresso shots se commits bante hain 🚀",
            "Coffee me sugar kam rakhna, bug dhoondhne me focus zaroori hai 🔍",
            "Chalo koi na, beverage chahe jo ho, code clean hona chahiye 🤝",
            "Black coffee energy: Latency zero aur focus 100% rehta hai ⚡",
            "Coffee cup ready rakh lo, project discussion lambi chalne wali hai ☕"
        ],
        "en": [
            "Traitor! But coffee is accepted as long as tests pass ☕😜",
            "Coffee enthusiast spotted! Don't let caffeine jitter crash prod servers 😂",
            "Tea passed over? Mild heartbreak, but espresso remains respectable ☕",
            "Silicon Valley style coder! Fueled by double espresso shots and vision 🚀",
            "Hold the sugar, high focus is mandatory when debugging complex trees 🔍",
            "No hard feelings: Whatever the fuel, clean code is what counts 🤝",
            "Black coffee energy: Zero latency and 100% continuous concentration ⚡",
            "Keep the coffee mug filled, our engineering discussion has momentum ☕"
        ]
    },

    "prank_project_prompt": {
        "in": [
            "Kya aapke liye agla killer project lau? 🚀",
            "Portfolio ka agla featured project dekhna chahte ho? 📂",
            "Next project reveal karun? Hardware aur AI ka solid combo hai ⚡",
            "Agla project screen pe open kar du? Bas 'Haan' bolo 💡",
            "Ek aur technical case study inspect karne ka mood hai? 🔍",
            "Curious ho na? Agla project aur bhi zyada impressive hai ✨",
            "Next build presentation ready hai! Kya launch karu? 🚀",
            "Projects ki library badi hai: Next masterpiece dekhna hai dost? 🎨"
        ],
        "en": [
            "Shall I bring up the next featured project for you? 🚀",
            "Ready to inspect the next featured systems build in this catalog? 📂",
            "Reveal the next project? It features a powerful hardware-AI pairing ⚡",
            "Open the next project modal right now? Say the word 💡",
            "In the mood to inspect another rigorous engineering case study? 🔍",
            "Naturally curious? The upcoming project is even more impressive ✨",
            "Next technical presentation queued up! Ready to launch? 🚀",
            "Deep project catalog: Care to inspect the next technical build? 🎨"
        ]
    },

    "prank_project_yes": {
        "in": [
            "Ye dekho! Next project specifications aapke saamne load ho gayi 📂✨",
            "Boom! Agla project live ho gaya, padho aur inspect karo 🔍",
            "Loading complete! Har architecture detail crystal clear hai boss ⚡",
            "Ye project dekh ke aapka dil khush ho jayega, guaranteed hai 🏆",
            "Technical excellence in action: Next project screen pe present hai 🚀",
            "Code aur design dono 10/10: Dekho aur feedback zaroor dena 💬",
            "Swagat hai agle project me! Innovation kabhi rukti nahi Max ki 💡",
            "Full details live: Problem, solution, aur impact sab mapped hai 🎯"
        ],
        "en": [
            "Here it is! Next project technical specifications loaded right up 📂✨",
            "Boom! Next architecture loaded live, dive in and inspect the code 🔍",
            "Specs loaded! Every architectural layer mapped out with precision ⚡",
            "This build will genuinely delight your engineering instincts, guaranteed 🏆",
            "Technical craft in action: Next project presented directly on screen 🚀",
            "Both architecture and code quality at 10/10: Inspect and review 💬",
            "Welcome to the next milestone! Continuous innovation from Mahendra Mali 💡",
            "Complete spec live: Problem statement, solution, and verified impact 🎯"
        ]
    },

    "prank_project_no": {
        "in": [
            "Theek hai! Ready ho to project card pe tap kar dena 🧭",
            "Pacing acchi hai! Pehle wala project shanti se digest kar lo ☕",
            "No problem! Main yahi dock me khada hu, aaram se ghoomo 🛋️",
            "Slow and steady inspection: Veteran managers ki yahi pehchan hai 👓",
            "Aaram se explore karo dost! Koi jaldi nahi hai 🌴",
            "Standing by! Naya project dekhna ho to mujhe bula lena 🤖",
            "Take your time: Har card me detailed engineering facts bhare hain 📜",
            "Robot chilling mode: Aapke instructions ka intezar kar raha hu ⏳"
        ],
        "en": [
            "All good, standing by! Tap any card whenever you're ready 🧭",
            "Paced review: Take your time digesting the previous case study ☕",
            "No problem! Standing by calmly in dock, explore at your leisure 🛋️",
            "Deliberate, thorough inspection: Hallmark of a great engineering lead 👓",
            "Explore comfortably, friend! No rush to jump across sections 🌴",
            "Standing by! Whenever you want next technical tour, call on me 🤖",
            "Take your time: Every card contains detailed engineering metrics 📜",
            "Mascot in rest mode: Awaiting your next navigation command ⏳"
        ]
    },

    "prank_bug_prompt": {
        "in": [
            "Portfolio me bug dhoondh ke dikhaun? 🐛",
            "Chalo meri AI scan se bug hunting karte hain, shuru karein? 🔍",
            "Kya aapko lagta hai is site me ek bhi error chhupega? 🧐",
            "Live automated bug scan run karu kya? 2 second lagenge ⚡",
            "Zero bugs challenge! Dhoondh ke dikhau ya khud check karoge? 🛡️",
            "Console audit chalayein? Dekhte hain kitne errors milte hain 💻",
            "Ek fun audit: Bug hunting mode activate karun kya? 🐞",
            "Bugs vs Clean Code: Kaun jeetega? Check karte hain 🏆"
        ],
        "en": [
            "Want me to search for bugs on this page? 🐛",
            "Launch an AI automated scan to hunt for hidden bugs? 🔍",
            "Do you suspect a single bug could hide in this architecture? 🧐",
            "Run a live automated diagnostics scan? Takes just two seconds ⚡",
            "Zero bug challenge! Shall I search or will you inspect DevTools? 🛡️",
            "Trigger a console audit? Let's verify error-free execution together 💻",
            "Quick diagnostics challenge: Activate automated bug hunting mode? 🐞",
            "Bugs versus Clean Architecture: Want to see who wins? 🏆"
        ]
    },

    "prank_bug_yes": {
        "in": [
            "Radar scan complete: 0 errors, 0 memory leaks, 100% clean! 🛡️",
            "Haha! Dhoondha par ek bhi bug nahi mila! Pure vanilla perfection ⚡",
            "Console check: Zero warnings, zero crashes, pure stable performance 💻",
            "Max code me bug dhoondhna desert me water dhoondhne jaisa hai 😂",
            "Audit complete: 50/50 test pass! Code ekdum rock solid hai 🏆",
            "Memory leak test passed: Garbage collector aaram se so raha 💤",
            "Bug hunter robot reports: Sabhi systems green aur optimized hain 🟢",
            "Clean architecture ka yahi to fayda hai: Zero production panics! ✨"
        ],
        "en": [
            "Radar scan complete: 0 errors, 0 memory leaks, 100% clean! 🛡️",
            "Haha! Searched everywhere, zero bugs found! Pure vanilla speed ⚡",
            "Console check verified: Zero warnings, zero unhandled rejections 💻",
            "Hunting bugs in Max's code is finding needles in clean rooms 😂",
            "Audit passed: 50/50 tests green! Production code is rock solid 🏆",
            "Memory stability verified: Garbage collector running in total peace 💤",
            "Diagnostics report: All system modules nominal and optimized 🟢",
            "The payoff of disciplined engineering: Zero production fire drills! ✨"
        ]
    },

    "prank_bug_no": {
        "in": [
            "Pehle se pata tha! Verified architecture me bugs nahi aate boss 😎",
            "Confidence 100%! Aap jante ho ki Max ka code production-grade hai 🏆",
            "Smart choice! Trust in verified tests and clean documentation 📜",
            "Bilkul sahi! Time waste kyu jab quality pehle se guaranteed hai ✨",
            "Smug robot nods: Quality code needs no defensive justifications 💡",
            "Aapka trust jeet liya! Chalo ab offer letter pe signature karein 🤝",
            "Clean code lovers recognize clean code instantly, respect! 🫡",
            "Verified confidence: High standards always speak for themselves 🌟"
        ],
        "en": [
            "You knew already! High standards leave zero room for bugs 😎",
            "100% confidence! You recognize production-grade craftsmanship 🏆",
            "Smart choice! Trust backed by verified tests and clean documentation 📜",
            "Exactly right! No need to hunt when high quality is self-evident ✨",
            "Smug mascot approval: Quality code requires zero defensive excuses 💡",
            "Trust earned! Time to seal the partnership with an offer letter 🤝",
            "Clean code connoisseurs recognize clean architecture instantly, respect! 🫡",
            "Unshakable confidence: High engineering standards always speak for themselves 🌟"
        ]
    }
}

# Merge new triggers
CAPTIONS.update(NEW_TRIGGERS)

# Validation logic
def validate_dataset():
    total_triggers = len(CAPTIONS)
    total_captions = 0
    issues = []
    dash_regex = re.compile(r'[\u2013\u2014]')

    # Verbatim user exemptions
    EXEMPT = [
        'Download ho gaya? Ab mail bhi kar do, main wait kar raha hu 📧'
    ]

    for trigger, lang_map in CAPTIONS.items():
        in_list = lang_map.get("in", [])
        en_list = lang_map.get("en", [])

        if len(in_list) < 8:
            issues.append(f"Trigger '{trigger}' has only {len(in_list)} IN captions (min 8 required)")
        if len(en_list) < 8:
            issues.append(f"Trigger '{trigger}' has only {len(en_list)} EN captions (min 8 required)")

        all_caps = in_list + en_list
        regional = lang_map.get("regional", {})
        for reg_k, reg_v in regional.items():
            all_caps.extend(reg_v)

        for cap in all_caps:
            total_captions += 1
            words = cap.split()
            if len(words) > 12 and cap not in EXEMPT:
                issues.append(f"Trigger '{trigger}' caption too long ({len(words)} words): '{cap}'")
            if dash_regex.search(cap):
                issues.append(f"Trigger '{trigger}' contains em/en-dash: '{cap}'")

    print(f"Validated {total_triggers} triggers with {total_captions} total captions.")
    if issues:
        print("ISSUES DETECTED:")
        for iss in issues[:30]:
            print(" -", iss)
        if len(issues) > 30:
            print(f" ... and {len(issues) - 30} more issues")
        raise SystemExit(1)
    else:
        print("ALL CRITERIA PASSED: Zero dashes, word count <= 12, min 8 captions per language.")

    # Export to js/captions.js
    js_content = "/* Robot captions dataset */\n"
    js_content += "window.MAXHIVE_CAPTIONS = " + json.dumps(CAPTIONS, indent=2, ensure_ascii=False) + ";\n"

    with open("js/captions.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Exported to js/captions.js successfully!")

    # Also update tools/build_robot_captions.py
    py_content = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nimport json\nimport re\n\n"
    py_content += "CAPTIONS_DATA = " + json.dumps(CAPTIONS, indent=4, ensure_ascii=False) + "\n\n"
    py_content += """def validate_captions():
    total_triggers = len(CAPTIONS_DATA)
    total_captions = 0
    issues = []
    dash_regex = re.compile(r'[\\u2013\\u2014]')
    EXEMPT = ['Download ho gaya? Ab mail bhi kar do, main wait kar raha hu 📧']

    for trigger, lang_map in CAPTIONS_DATA.items():
        in_list = lang_map.get("in", [])
        en_list = lang_map.get("en", [])
        if len(in_list) < 8:
            issues.append(f"Trigger '{trigger}' has only {len(in_list)} IN captions (min 8 required)")
        if len(en_list) < 8:
            issues.append(f"Trigger '{trigger}' has only {len(en_list)} EN captions (min 8 required)")

        all_caps = in_list + en_list
        for reg_k, reg_v in lang_map.get("regional", {}).items():
            all_caps.extend(reg_v)

        for cap in all_caps:
            total_captions += 1
            words = cap.split()
            if len(words) > 12 and cap not in EXEMPT:
                issues.append(f"Trigger '{trigger}' caption too long ({len(words)} words): '{cap}'")
            if dash_regex.search(cap):
                issues.append(f"Trigger '{trigger}' contains em/en-dash: '{cap}'")

    print(f"Validated {total_triggers} triggers with {total_captions} total captions.")
    if issues:
        print("ISSUES DETECTED:")
        for iss in issues[:30]:
            print(" -", iss)
        raise SystemExit(1)
    else:
        print("ALL CRITERIA PASSED: Zero dashes, word count <= 12, min 8 captions per language.")

    js_content = "/* Robot captions dataset */\\n"
    js_content += "window.MAXHIVE_CAPTIONS = " + json.dumps(CAPTIONS_DATA, indent=2, ensure_ascii=False) + ";\\n"
    with open("js/captions.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Exported to js/captions.js successfully!")

if __name__ == "__main__":
    validate_captions()
"""
    with open("tools/build_robot_captions.py", "w", encoding="utf-8") as f:
        f.write(py_content)
    print("Updated tools/build_robot_captions.py successfully!")

if __name__ == "__main__":
    validate_dataset()
