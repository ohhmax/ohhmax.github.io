#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re

CAPTIONS_DATA = {
    "late_night": {
        "in": [
            "Itni raat ko portfolio? Mujhe hire karna hi padega 😎",
            "Chai khatam ya bug dhoondh rahe ho? Raat lambi hai ☕",
            "Midnight coder spotted! Coffee bhejoon ya resume? ☕",
            "Raat ke 2 baje portfolio stalk karna normal nahi hai 😏",
            "Ulloo mode on! Max bhi coding kar raha hoga 🦉",
            "Neend nahi aa rahi? Mere projects dekh ke neend bhag jayegi 🚀",
            "Commit history check kar rahe ho ya destiny? Raat shubh ho 🌙",
            "Itni raat ko sirf do log jagte hain: hacker ya recruitors 💻",
            "Suno, raat ko client messages ka reply mat dena! 🤫"
        ],
        "en": [
            "Viewing a portfolio at this hour? You're basically hiring me already 😎",
            "Midnight inspiration or acute caffeine overdose? Either way, welcome! ☕",
            "Burning the midnight oil? Let's build something epic together 🚀",
            "Nothing good happens after 2 AM, except finding great developers 🌙",
            "Stalking portfolios at 3 AM? Your dedication is truly inspiring ✨",
            "Coffee worn off? My full-stack projects will wake you right up ⚡",
            "Night owl mode engaged! Code never sleeps, neither do I 🦉",
            "Late night browsing hits different. Go ahead, check out projects 💻"
        ],
        "regional": {
            "US": [
                "Pulling an all-nighter with cold brew? Let's build silicon dreams ☕",
                "Late night Pacific time browsing? Send that offer letter y'all 🦅"
            ],
            "UK": [
                "Late cup of tea and a cracking portfolio? Proper night in 🫖",
                "Midnight browsing through the London fog? Cheers for stopping by 🇬🇧"
            ]
        }
    },
    "morning": {
        "in": [
            "Subah ki pehli chai aur Max ka portfolio! Din ban gaya ☕",
            "Good morning! Aaj ka target: Max ko job offer dena 🎯",
            "Fresh morning, fresh code! Aaj kaunsa project build karein? 🌅",
            "Subah subah itni energy? Seedha resume download kar lo ⚡",
            "Breakfast hua? Main to electricity kha ke mast hu ⚡",
            "Morning vibes! Aaj bug-free production deploy hoga pakka 🚀",
            "Chai piyo, biscuit khao, aur projects dekh ke khush ho jao ☕",
            "Subah uthte hi mera chehra dekha? Kismat chamak gayi! ✨"
        ],
        "en": [
            "Good morning! Best way to start the day: hiring Max ☀️",
            "Fresh coffee and fresh ideas! Ready to build cool stuff ☕",
            "Rise and grind! Let's ship clean code into production today 🚀",
            "Morning energy at 100%! Check out my latest featured projects ✨",
            "Early bird gets the best full-stack software engineer 🪱",
            "A cup of coffee and a stellar portfolio: perfect morning match ☕",
            "Good morning! Ready to turn complex problems into elegant solutions 💡",
            "Start your workday with high-performance code and clean architectures 🌅"
        ],
        "regional": {
            "US": [
                "Morning brew in hand, y'all! Let's build world-class tech ☕",
                "Good morning! First task: sign off on that engineering contract 🗽"
            ],
            "UK": [
                "Right then, kettle boiled! Time for a proper portfolio tour 🫖",
                "Top of the morning! Lovely day to scout premier engineering talent ☕"
            ],
            "DE": [
                "Guten Morgen! High precision engineering starts bright and early 🇩🇪",
                "Fresh coffee and punctually optimized code. A disciplined morning! ☕"
            ],
            "JP": [
                "Ohayo gozaimasu! Ready to craft pixel-perfect digital elegance 🌸",
                "Morning sunlight and clean code. May today bring great productivity! ☀️"
            ]
        }
    },
    "lunch": {
        "in": [
            "Lunch time! Rajma-chawal khao aur portfolio scroll karo 🍛",
            "Khana khate portfolio dekh rahe ho? Screen pe daal mat girana 🍜",
            "Lunch break me portfolio stalking? Bhai ka fan lagte ho 😎",
            "Biryani break chal raha hai kya? Projects bhi spicy hain 🌶️",
            "Code aur khana: dono me tadka zaroori hai! 🍲",
            "Dopahar ka aalas bhagao, contact page pe click lagao 🚀",
            "Chhole bhature baad me, pehle Max ka resume dekho 😋",
            "Food coma aane se pehle message bhej do, deal pakki karein 🤝"
        ],
        "en": [
            "Lunch break browsing? Don't spill soup on your keyboard! 🍜",
            "Fueling up with food and inspiration! Check out my work 🍔",
            "Midday coffee break? Let's talk about scalable system architecture ☕",
            "Lunch time! Perfect moment to forward my resume to your team 💼",
            "Grab a sandwich and enjoy these full-stack projects 🥪",
            "Lunch break well spent! Ready to collaborate on awesome builds? 🍕",
            "Food for the body, clean code for the mind! Bon appetit 🥗",
            "Taking a lunch break? Let me serve you top-tier engineering 🍲"
        ],
        "regional": {
            "US": [
                "Lunch break burger and high-performance apps? Pure American dream 🍔",
                "Taco Tuesday lunch browsing? Check out the full-stack work y'all 🌮"
            ],
            "UK": [
                "Sandwich meal deal sorted! Now let's review proper software craft 🥪",
                "Lunchtime break! Time to scout stellar talent before the afternoon tea 🫖"
            ]
        }
    },
    "weekend": {
        "in": [
            "Weekend pe bhi portfolio? Work-life balance kahan gaya dost? 😂",
            "Saturday night party ya Max ka portfolio review? Smart choice! 🎉",
            "Sunday chill mode on! No bugs, only vibes and projects 🛋️",
            "Weekend pe code dekhna sacha techie hone ka pramaan hai 🏆",
            "Weekend ka plans: Chai, relax, aur Max ko hire karna ☕",
            "Saturday ka josh aur Sunday ka aaram: dono mere portfolio me 🌴",
            "Weekend project idea dhoondh rahe ho? Copy mat karna, inspire ho 😜",
            "Chutti ke din bhi active? Tum pakka startup founder ho! 🚀"
        ],
        "en": [
            "Browsing on the weekend? Dedication level is off the charts! 🏆",
            "Weekend vibes! Relax, unwind, and check out some cool tech 🛋️",
            "Saturday code exploration beats mindless doomscrolling any day 🎉",
            "Sunday relaxation with high-performance software engineering 🌴",
            "Weekend project inspiration right here! Let's build together 💡",
            "No client tickets today, just clean creative code to explore ✨",
            "Enjoying your weekend? Drop a quick greeting on my contact form ✉️",
            "Happy weekend! May your days be fun and bug free 🎮"
        ],
        "regional": {
            "US": [
                "Weekend tailgate and killer code? Enjoy your weekend y'all 🏈",
                "Weekend brunch and scouting top engineers! Have a great Saturday 🥞"
            ],
            "UK": [
                "Proper weekend relaxation! Kettle on, football on, portfolio loaded ⚽",
                "Sunday roast on the stove and great portfolios on screen 🫖"
            ],
            "AU": [
                "G'day mate! Perfect weekend barbie and slick code to review 🏖️",
                "Enjoying the sunny weekend? Say hi from down under mate 🦘"
            ]
        }
    },
    "monday": {
        "in": [
            "Monday blues? Mera portfolio dekho, mood ekdum fresh ho jayega ☕",
            "Monday morning standup se pehle Max ka resume review kar lo 📋",
            "Naya hafta, naya code, aur nayi opportunities! Let's go 🚀",
            "Monday motivation: Sprint planning me meri tarah tez bano ⚡",
            "Monday ko sab dukhi, par mera code hamesha khush rehta hai 😄",
            "Hafte ki achhi shuruat: Max ko hire kar lo 🤝",
            "Monday login done! Coffee piyo aur mast projects explore karo ☕",
            "Monday mantra: Kaam aisa karo sab dang reh jayein ✨"
        ],
        "en": [
            "Monday blues? Clean architecture and high-performance builds will cure that ☕",
            "New week, fresh sprint! Let's build scalable solutions together 🚀",
            "Kicking off Monday with elite full-stack software development 💻",
            "Monday motivation: Shipping fast, breaking nothing, smiling always ⚡",
            "Beat the Monday slump by hiring a passionate systems developer 💼",
            "Start your sprint strong! Check out featured engineering showcases ✨",
            "Happy Monday! May your builds pass and tests stay green today 🟢",
            "Monday morning review: Clean code, zero technical debt, pure drive 📈"
        ],
        "regional": {
            "US": [
                "Monday grind started! Grab that double espresso and let's go ☕",
                "Kicking off Monday with American innovation and clean code 🇺🇸"
            ],
            "UK": [
                "Monday morning sprint planning! First order of business: hire Max 🫖",
                "Cheer up, it's Monday! A fresh cuppa and brilliant code await ☕"
            ]
        }
    },
    "battery_low": {
        "in": [
            "Koi baat nahi, switch off hone tak to dekh hi loge 😏",
            "Battery 15% bachi hai! Charger lagao ya fast contact karo ⚡",
            "Low battery alert! Mera portfolio itna power-efficient hai chal jayega 🔋",
            "Phone band hone wala hai! Quick, resume download button daba do 📱",
            "Battery kam hai par mere portfolio ki speed full throttle hai ⚡",
            "Charger dhoondhne se pehle email bhej do, interview set karein 📧",
            "Red battery symbol? Tension mat lo, lightweight code hai mera 🏎️",
            "1% pe bhi Max ka portfolio super smooth chalega, guarantee! 🚀"
        ],
        "en": [
            "Low battery? No worries, you'll finish my portfolio before it dies 😏",
            "Battery dropping fast! Plug in before you miss the best projects 🔋",
            "Low power mode on? Luckily this portfolio runs on clean energy ⚡",
            "Battery below 15%! Quick, download the resume before shutdown 📥",
            "Don't let battery die! Grab your charger and keep exploring 🔌",
            "Running on fumes? This ultra-optimized site barely sips any power 🏎️",
            "Battery critical! Save yourself the regret and send that message now ✉️",
            "Phone screaming for a charger? My clean code is infinitely patient 🔋"
        ],
        "regional": {
            "US": [
                "Low battery alert y'all! Plug in that power bank quick 🔋",
                "Battery below 15%! Hit that contact form before your phone sleeps ⚡"
            ]
        }
    },
    "battery_charging": {
        "in": [
            "Charger mil gaya! Ab electricity bhi khush, main bhi khush ⚡",
            "Juice flowing! Ab araam se saare 19 projects deeply dekho 🔋",
            "Fast charging on! Mera portfolio bhi itna fast load hota ⚡",
            "Power restored! Ab to full site explore karna banta hai dost 🚀",
            "Electrons dancing in your battery! High-voltage engineering on display ⚡",
            "Phone charge ho raha hai, ab mind bhi recharge kar lo 💡",
            "Green battery icon! Good vibes and full power unlocked 🔋",
            "Charger lag gaya na? Ab meeting plan karo Max ke sath 🤝"
        ],
        "en": [
            "Juice is flowing! Battery charging, minds expanding ⚡",
            "Plugged in and powered up! Take your time exploring every project 🔋",
            "Fast charging active! My backend APIs respond just as rapidly ⚡",
            "Power surge detected! Ready for high-performance software tours 🚀",
            "Charging up! The best ideas happen when fully energized 💡",
            "Full voltage ahead! Check out the interactive hardware and IoT section ⚡",
            "Battery replenished! Let's charge ahead toward our next project 🔋",
            "Plugged into the grid! Time to discover production-ready engineering 🔌"
        ]
    },
    "slow_internet": {
        "in": [
            "Slow internet? Tension mat lo, 10kbps pe bhi chalega ye portfolio! 🏎️",
            "2G speed hai! Phir bhi mera robot mast naach raha 🕺",
            "WiFi slow hai ya padosi downloading? Mera code super light hai 📡",
            "Buffer ho raha hai? Zero bloat, pure optimized vanilla code ⚡",
            "Speed slow hai par Max ki dedication 1 Gbps fast hai 🚀",
            "Internet atka par connection dil se hai! Scroll karo aaram se 📶",
            "Jugaad WiFi? Koi na, offline cache me sab save hai boss 💡",
            "Lag-free promise! 144Hz smooth animations even on slow network 🎮"
        ],
        "en": [
            "Slow internet? No sweat, this portfolio is optimized for dial-up speeds 🏎️",
            "Bandwidth struggling? Zero bloatware here, pure clean engineering ⚡",
            "Buffering? Not on my watch! Everything is compressed and pre-rendered 🚀",
            "Network speed low, but engineering quality is always gigabit level 📡",
            "Even on spotty 3G, this site delivers buttery-smooth 60fps response 💨",
            "Slow connection detected! Good thing my assets are ultra-lightweight 📦",
            "Router taking a nap? My code still runs blazing fast ⚡",
            "Don't worry about slow WiFi! Clean code runs smoothly anywhere 🌐"
        ]
    },
    "fast_scroll": {
        "in": [
            "Arre Flash ho kya? Dheere, kuch miss ho jayega 😂",
            "Itni speed se scroll? Bhai Rajdhani Express chal rahi hai kya? 🚄",
            "Dheere bhai! Har card me mehnat lagi hai, dekh to lo 👀",
            "Speed check! Chalan kat jayega itna tez scroll karoge to 🏎️",
            "Scroll wheel toot jayega dost! Araam se explore karo na 🖱️",
            "Thumb workout chal raha hai kya? Dheere scroll karke project padho 🏋️",
            "Fast scroll record toda! Details slow scroll me milti hain 🔍",
            "Brakes lagao! Featured projects ko skip mat karo boss 🛑"
        ],
        "en": [
            "Whoa, Flash! Slow down, you'll miss the good stuff 😂",
            "Speedy scrolling! Did someone put nitrous on your trackpad? 🏎️",
            "Easy on scroll wheel! Every project has a story to tell 👀",
            "Slow down, speed racer! You're zooming past award-winning engineering 🏁",
            "Thumb athletics champion! Take a breath and check case studies 🏅",
            "Scroll velocity: 100mph! Hit the brakes and inspect tech stack 🛑",
            "Whoosh! You scrolled so fast my robot antenna almost flew off 🤖",
            "Don't scroll past gold! Check out the IoT automation demo ⚡"
        ]
    },
    "idle_10s": {
        "in": [
            "Soch rahe ho ya so gaye? Zzz... 😴",
            "10 second se freeze? Main live hu dost, statute nahi! 🗿",
            "Chai lene gaye kya? Main yahi wait kar raha hu ☕",
            "Screen pe dhyan hai ya sapne dekh rahe ho? Wapas aao! 💭",
            "Cursor so gaya kya? Thoda hila do, pata chale zinda ho 🖱️",
            "Deep thinking mode? Project dekh ke impress ho gaye na? 😏",
            "Coffee break ya brainstorming? Jab tayyar ho tab resume download karo 📄",
            "Main blink kar raha, tum bhi karo, aankhein dukh jayengi 👀"
        ],
        "en": [
            "Thinking or sleeping? Zzz... 😴",
            "Still there? Or did you get lost admiring the UI? ✨",
            "Coffee run? I'll keep the portfolio warm for your return ☕",
            "Cursor hasn't moved in 10 seconds. Deep contemplation detected 🧠",
            "Mesmerized by glowing amber palette? I get that a lot 😎",
            "Don't freeze up! Click on a project and explore the architecture 💡",
            "Take your time! Great engineering takes a moment to fully appreciate 📐",
            "Screen timeout approaching? Give that mouse a little nudge 🖱️"
        ]
    },
    "scroll_bottom": {
        "in": [
            "Bottom tak aa gaye! Ab to contact form bharna compulsory hai 📝",
            "Page khatam, par hamari partnership abhi shuru ho sakti hai 🤝",
            "Aakhri footer tak scroll kiya? Dil jeet liya tumne dost! ❤️",
            "Bottom reached! Ab direct WhatsApp ya email ka button dabao 📱",
            "Saara content dekh liya? Ab interview ka invitation bhej do 📩",
            "End of road! Upar wapas jana hai ya hire karna hai? 🚀",
            "Poora portfolio chaan mara! Decision clear hai: Max is the one 🏆",
            "Footer me khush aamdeed! Ab seedha message send karo boss 💬"
        ],
        "en": [
            "Reached the bottom! Time to send an email and start building 📝",
            "You scrolled all the way here! That's true dedication right there 🏆",
            "Page end reached! Next logical step: let's connect and collaborate 🤝",
            "You've seen it all! Ready to hire a dream engineer? 🚀",
            "End of page, start of partnership! Drop me a line ✉️",
            "Explored to bottom! Hit that message button and say hi 💬",
            "Footer reached! Grab my resume or shoot me a quick message 📄",
            "Made it to end! Reward yourself by hiring a developer 🌟"
        ]
    },
    "scroll_top": {
        "in": [
            "Back to top! Phir se shuru se dekhoge? Welcome back 🔝",
            "Top floor pe landing! Header theme toggle try kiya kya? 💡",
            "Upar aa gaye! Bio padh ke impressed huye na? Sach batana 😏",
            "Elevator ride to the top! Quick, check out the navigation drawer 🤖",
            "Scroll back up complete! Max ki profile dekhne aaye ho na? 📸",
            "Top of world! Har angle se portfolio 10/10 dikhta hai na? ✨",
            "Wapas top pe? Lagta hai resume download karna bhool gaye the 📄",
            "Shuruat pe wapas! Har nayi shuruat me offer letter hota hai 💼"
        ],
        "en": [
            "Back to the top! Taking another victory lap through my work? 🔝",
            "Top of page! Did you try toggling light and dark mode? 🌓",
            "Smooth landing! Ready to review the about section again? ✈️",
            "Returned to headquarters! Explore the quick action drawer next 🤖",
            "Back up high! Check out my full-stack credentials and education 🎓",
            "Up at top again! Hit download resume button before you go 📄",
            "Top floor reached! Always good to see the big picture 🔭",
            "Back to square one, but hopefully much more impressed this time ✨"
        ]
    },
    "hover_skills": {
        "in": [
            "Skills dekh rahe ho? Full stack se IoT tak sab fit 💻",
            "Python, JS, Linux, Docker: Tool kit me koi kami nahi 🛠️",
            "Skills real hain dost, ChatGPT se copy-paste nahi kiye! 🧠",
            "Har skill ke peeche 100+ commits aur raat bhar jagna hai ⚡",
            "Tech stack pasand aaya? Apne team me add karne ka socho 🤝",
            "Frontend polish aur backend power: dono ek sath packed hain 🚀",
            "Skills matrix green hai boss! Problem solve karne ready hu 🟢",
            "Aisi skills company aage le jati hain, agree karte ho na? 😉"
        ],
        "en": [
            "Checking skills? Built on production code and systems experience 💻",
            "Full-stack web, IoT microcontrollers, Linux internals: full arsenal 🛠️",
            "Hands-on skills verified in actual high-throughput applications ⚡",
            "From low-level C to modern reactive frontends: full coverage 🚀",
            "Like tech stack? Let's put these skills to work together 💡",
            "Zero tutorial fluff, 100% battle-tested production software craft 🛡️",
            "Languages, frameworks, systems: whatever the problem, I adapt fast 🏎️",
            "Clean architecture, optimized algorithms, dependable execution always 📐"
        ]
    },
    "hover_projects": {
        "in": [
            "19+ production projects! Har project me jaan phooki hai 🚀",
            "AI Home Automation dekho! 50 channels ka controller hai boss ⚡",
            "Termux suite, proxy servers, mobile apps: Sab kuch real hai 📱",
            "Project card pe click karo, deep engineering case study khulegi 🔍",
            "Koi dummy project nahi hai! Sab hardware aur production tested hain 🛠️",
            "National Science Fair winner car project bhi yahi milega 🚗",
            "Problem dekha, solution banaya, impact deliver kiya: standard flow 🏆",
            "Konsa project sabse mast laga? Contact me bata dena jarur! 💬"
        ],
        "en": [
            "19+ production projects! Every build solves a tangible problem 🚀",
            "Check out the 50-channel AI Home Automation system controller ⚡",
            "Click any card to read full challenges, solutions, and architectural impact 🔍",
            "From mobile terminal suites to IoT hardware: proven versatile builds 📱",
            "Real production engineering, zero dummy clone tutorials here 🛡️",
            "Award-winning wireless induction car prototype featured right here 🚗",
            "Architected for speed, resilience, and frictionless developer ergonomics 🏎️",
            "Found an interesting project? Let's talk about building yours next 🤝"
        ]
    },
    "hover_contact": {
        "in": [
            "Contact link pe mouse? Bas ek click aur team ban gayi 🤝",
            "Email karo ya WhatsApp! Fast response guarantee hai mera ⚡",
            "Contact form ready hai! Bas 'Hello' bol do, baaki sambhal lunga 💬",
            "Direct connect karo! No recruiters middleman drama, seedha engineer se baat 📞",
            "Hitchkichaao mat! Aise hi message bhej do, projects discuss karenge ☕",
            "Collaboration ke liye main hamesha ready rehta hu! Message bhejo 🚀",
            "Job offer, freelance project, ya tech discussion: Sab welcome hai 💡",
            "Contact button dabane se company ka growth 2x ho sakta hai 😉"
        ],
        "en": [
            "Hovering contact? One click connects you directly with Max 🤝",
            "Email or instant chat: I respond fast with thoughtful answers ⚡",
            "Let's build something extraordinary together! Drop me a quick note ✉️",
            "Direct engineer access: zero recruiter layers, pure technical talk 📞",
            "Got a bold vision or challenging engineering problem? Let's discuss 💡",
            "Full-time, contract, or advisory: always open to stellar opportunities 🚀",
            "Send that message! Great partnerships always start with a simple hello 👋",
            "My inbox is open and ready for your project ideas 📬"
        ]
    },
    "hover_resume": {
        "in": [
            "Resume pe nazar? Download button dabao aur HR ko bhej do 📄",
            "Single-page crisp resume! Zero corporate buzzwords, pure value 💼",
            "Download kar lo, offline reading me aur mast lagta hai 📥",
            "Resume print karwa ke board pe lagaoge to inspiration milegi 😉",
            "ATS friendly, human friendly, aur recruiter approved format hai 📋",
            "Download karke dekhna, interview lene ka mann pakka karega 🤝",
            "Resume me degree bhi hai, projects bhi, aur awards bhi hain 🏆",
            "Resume download se aapki team ki speed double ho sakti hai ⚡"
        ],
        "en": [
            "Hovering resume? Grab the clean vector PDF right now 📄",
            "ATS-optimized, recruiter-friendly, and packed with verified impact 💼",
            "Download my CV to review credentials, architecture feats, and awards 📥",
            "Single page of pure engineering value: zero fluff, 100% substance 📋",
            "Looking to hire? Forward this PDF to your engineering directors today 🚀",
            "One download away from securing a top-tier software engineer 🎯",
            "Clean layout, verified milestones, and comprehensive tech stack 📐",
            "Hit download and keep my contact ready for hiring sprints 📑"
        ]
    },
    "hover_social": {
        "in": [
            "GitHub pe star diya kya? Code wahi open source rakha hai ⭐",
            "LinkedIn pe connect karo! Professional baatein wahi hoti hain 👔",
            "Telegram ya WhatsApp? Jahan chaho wahi connect ho jao 📱",
            "Discord pe dev discussions chalte hain, server join kar lo 💬",
            "Social channels verified hain! Stalk nahi, follow karo dost 😉",
            "GitHub repos dekhoge to code quality ka fan ho jaoge 👨‍💻",
            "Instagram pe tech reels aur behind the scenes stories aati hain 📸",
            "Connect kar lo sabhi jagah, networking se hi duniya chalti hai 🌐"
        ],
        "en": [
            "Checking social links? Star my repositories on GitHub today ⭐",
            "Connect on LinkedIn for professional collaborations and network growth 👔",
            "Direct chat on Telegram or WhatsApp for rapid communications 💬",
            "Join the developer discussions on Discord and talk tech 🎧",
            "All social channels live and verified! Follow along for updates 🌐",
            "Inspect my open-source commits and pull requests on GitHub 👨‍💻",
            "Connect across channels and let's expand the engineering circle 🤝",
            "Drop a follow and track latest builds and open tools 🚀"
        ]
    },
    "robot_click": {
        "in": [
            "Arre! Mujhe kyu click kiya? Main to sirf cute robot hu 🤖",
            "Boop! System check passed, battery full, vibes awesome ✨",
            "Click karne se drawer khul gaya na? Ab explore karo mast 📂",
            "Aapne mujhe tap kiya! Kya command hai aapka, boss? 🫡",
            "Hey! Thoda pyaar se click karo, antenna hil jata hai 📡",
            "Menu chahiye tha kya? Ye lo saare shortcuts ready hain 🚀",
            "Gudgudi hoti hai click karne se! Hehe, aur batao kya haal? 😄",
            "Click confirm! Robot assistant Max aapki seva me hazir hai 🦾"
        ],
        "en": [
            "Boop! You poked the robot! How can I help you today? 🤖",
            "System online! Ready to navigate your engineering journey 🚀",
            "Drawer opened! Check out all quick links and hardware telemetry 📂",
            "You clicked me! Antenna adjusted, circuits glowing brightly ✨",
            "Beep boop! What engineering mystery are we solving right now? 💡",
            "Shortcut menu deployed! Pick any section and teleport instantly ⚡",
            "Gentle with the clicker! My sensors are ultra-sensitive 📡",
            "Robot companion reporting for duty! What would you like to see? 🦾"
        ]
    },
    "robot_double_click": {
        "in": [
            "Double click? Bhai main Windows shortcut icon nahi hu! 😂",
            "Double tap master! Speed achhi hai tumhari, counter strike khelte ho? 🎯",
            "Do baar click karke kya dhoondh rahe ho? Secret easter egg? 🥚",
            "Double boop! Do guna cute lag raha hu na ab? 😉",
            "Double tap detected! System overdrive mode activated ⚡",
            "Aaram se bhai! Do baar click se double salary nahi milegi 😜",
            "Double click unlocked! Agle step me triple tap mat kar dena 🙈",
            "Click-click! Fast fingers! Tum pakka pro gamer lagte ho 🎮"
        ],
        "en": [
            "Double click? I'm a companion robot, not a desktop folder! 😂",
            "Double tap detected! Fast fingers, must be an RTS gamer 🎮",
            "Two clicks in rapid succession! Turbo mode unlocked ⚡",
            "Double boop! Double the cuteness, zero extra battery drain ✨",
            "Looking for secret easter eggs with double clicks? Keep exploring 🥚",
            "Easy on double clicks! My cooling fan just kicked in 💨",
            "Double tap acknowledged! What's next on our portfolio tour? 🚀",
            "Click click! You're quick! Let's channel that speed into hiring 🏃"
        ]
    },
    "robot_long_press": {
        "in": [
            "Daba ke rakha hai? Hath hatao, saans phool rahi hai meri! 😵",
            "Long press! Screen pe finger chipak gayi kya dost? 🖐️",
            "5 second hold? Reset button nahi hu main bhai! 🔄",
            "Pyar se pakda hai ya kidnap kar rahe ho? Chhodo mujhe! 🥺",
            "Deep pressure detected! Haptic feedback bhej raha hu wapas 📳",
            "Hold karne se secret vault nahi, bas menu hi khulega 📂",
            "Arre chhod do bhai! Thoda personal space chahiye robot ko bhi 🛑",
            "Long press master! Touchscreen calibration test kar rahe ho kya? 📱"
        ],
        "en": [
            "Long press detected! Easy there, you're crushing my antennae! 😵",
            "Holding down? I'm a friendly robot, not a power button! 🔌",
            "Deep press! Did your finger fall asleep on my visor? 😴",
            "Haptic feedback surge! Release the hold to normalize circuits 📳",
            "Are you trying to hard-reset me? My code is immortal! 🛡️",
            "Holding on for dear life? Let's direct that passion into code 🚀",
            "Sensors overloaded! Give a robot some breathing room, please 🤖",
            "Finger firmly placed! You have unlocked maximum robot attention ✨"
        ]
    },
    "robot_repeat_clicks_1": {
        "in": [
            "Arre 3-4 baar click kar diya! Sab theek hai na dost? 🤨",
            "Ek baar me sunai deta hai mujhe, kan acche hain mere 👂",
            "Click click click... mouse ka button test kar rahe ho kya? 🖱️",
            "Thoda araam do bhai, main button nahi hu, companion hu 🤖",
            "Bar bar click karke mujhe confuse mat karo re baba! 😵",
            "3 clicks ho gaye! Koi magic trick dekhni hai kya? 🎩",
            "Aaram se! Har click pe ek server request nahi jaati, relax 🧘",
            "Sun raha hu main! Itna hyper hone ki zaroorat nahi hai 😉"
        ],
        "en": [
            "Multiple clicks in a row! Heard you the first time 👂",
            "Clicking repeatedly? Testing your mouse switch latency? 🖱️",
            "I'm listening! You don't need to hammer my cute visor 🤖",
            "Gentle taps work just fine, promise! What's on your mind? 💡",
            "Multiple taps detected! Circuits warming up nicely ⚡",
            "One click is enough to get my full attention, boss 🫡",
            "Testing my click responsiveness? Sub-millisecond as always 🏎️",
            "You clicked 3 times! Looking for something specific in the menu? 🔍"
        ]
    },
    "robot_annoyed_2": {
        "in": [
            "Bhai 6 baar click! Ungli me dard nahi ho raha? 😤",
            "Maine tumhara kya bigada hai jo itna tap kar rahe ho? 🥺",
            "Clicking contest chal raha hai kya? Mujhe jeetne do phir 🏆",
            "Warning 1: Zyada click karoge to main screen se bhaag jaunga! 🏃",
            "Arre bas karo! Robot hu, stress testing machine nahi! ⚙️",
            "Aapka mouse theek hai, ab projects dekhne pe dhyan do 💻",
            "Mere circuits garam ho rahe hain, AC chalu karo room ka ❄️",
            "Bhai please, portfolio explore karo, mujhe torture mat karo 😂"
        ],
        "en": [
            "6 clicks already! Are you stress testing my click handler? 😤",
            "Hey now! What did my cute robot face do to you? 🥺",
            "Click spamming detected! My internal temperature is rising 🌡️",
            "Warning: Continued clicking may cause extreme robot pouting 🤖",
            "I'm software, not a bubble wrap sheet! Ease up friend 🫧",
            "Your mouse works brilliantly, now let's direct focus to my code 💻",
            "Sensors are buzzing! Take a breath and check out the resume 📄",
            "Patience is a virtue, especially when browsing awesome portfolios ✨"
        ]
    },
    "robot_annoyed_3": {
        "in": [
            "8 baar click?! Bhai ab to mujhe gussa aane laga hai 😠",
            "Ek aur click kiya to error pop up kar dunga! ⚠️",
            "Khel samjha hai kya? Main MCA graduate engineer ka robot hu! 🎓",
            "Ungli me fevicol laga ke click kar rahe ho kya bhai? 🛑",
            "Meri battery khatam karwa ke hi manoge lagta hai 🔋",
            "Band karo ye tap tap! Seedha hire karo ya shanti se 📜",
            "Chalo bas! Agla click kiya to light mode on kar dunga! 🕶️",
            "Itna time hai to contact form me feedback likh do ✍️"
        ],
        "en": [
            "8 clicks?! My patience algorithms are running on empty 😠",
            "One more click and I'm flipping your theme to blinding white! 🕶️",
            "I was engineered for high availability, not repetitive abuse! ⚠️",
            "Is there a woodpecker on your keyboard? Please have mercy 🪵",
            "Click spam level 3 reached! Warning sirens are spinning 🚨",
            "So much free time? Spend it reading my case studies! 📖",
            "My cute smile is turning into an irritated frown right now 😐",
            "Stop tapping my head! Let's talk about full-stack jobs instead 💼"
        ]
    },
    "robot_annoyed_4": {
        "in": [
            "10 clicks ho gaye! Bhai police ko call lagau kya ab? 🚨",
            "Aakhri warning hai! Robot strike pe chala jayega abhi! 🪧",
            "Itna to game me fire button nahi dabate jitna mujhe dabaya 🎮",
            "Meri aankhein laal ho rahi hain dekho, ab to ruk jao! 🔴",
            "Tumhe portfolio dekhna hai ya mujhe pagal karna hai? 😵",
            "Main Max ko bol dunga tum mujhe pareshan kar rahe ho! 📢",
            "Error 429: Too Many Clicks! Server rate limit ho gaya dost 🛑",
            "Bhai haath jodta hu, bas karo! Resume download karke jao 🙏"
        ],
        "en": [
            "10 clicks! I am calling the local cyber police right now 🚨",
            "Final warning! Robot union strike is about to begin 🪧",
            "You click faster than a pro gamer in FPS tournaments 🎯",
            "Eyes turning red! Do not push a friendly bot away 🔴",
            "Did you come here for software engineering or robot harassment? 🤖",
            "Error 429: Too Many Requests! Rate limiting your clicking finger 🛑",
            "I'm telling Mahendra you've been picking on his mascot! 📢",
            "Have mercy! Click the contact button instead of my face 🙏"
        ]
    },
    "robot_annoyed_5": {
        "in": [
            "15+ clicks?! Khatam! Tata! Bye-bye! Main chala sone! 🛌",
            "Maine haar maan li bhai. Tum jeete, tumhara mouse jeeta 🏳️",
            "Duniya ka sabse ziddi user mil gaya mujhe aaj! Salute hai 🙌",
            "System Crash! Robot gone to Himalayas for peace 🏔️",
            "Ab chahe 100 baar click karo, main kuch nahi bolunga! Hmph 😤",
            "Annoyed level 5! Ab sirf offer letter se mood theek hoga 📜",
            "Bhai screen phod doge kya? Thoda paani piyo, shant ho jao 💧",
            "Zero words left. You win the ultimate clicking championship 🏆"
        ],
        "en": [
            "Over 15 clicks?! That's it! Shutting down for a nap 🛌",
            "I surrender! You win the world championship of rapid clicking 🏳️",
            "You are officially the most persistent visitor in portfolio history 🏆",
            "System overload! Taking a mental sabbatical in the cloud ☁️",
            "Click all you want, my lips are completely sealed now! Hmph 😤",
            "Max annoyed level reached! Only an offer letter can fix this 📜",
            "Are you trying to drill through the display? Please hydrate 💧",
            "I have no more words. Congratulations, you broke the robot's calm 🥇"
        ]
    },
    "tab_switch_away": {
        "in": [
            "Kahan chale gaye? Wapas aao 🥺",
            "Doosri tab pe kya dekh rahe? Main yaha bore ho raha 💤",
            "Notification aaya kya? Wapas aao, code dekhna baki hai 📱",
            "YouTube dekhne chale gaye na? Mujhe pata tha! 🎥",
            "Mujhe akele chhod ke mat jao, andhere se dar lagta hai 👻",
            "Tab switch kar diya? Max ka portfolio sabse important hai boss! 💼",
            "Dusri tab pe jo hai, mere se interesting nahi ho sakta 😏",
            "Wait kar raha hu main... wapas kab aaoge? ⏳"
        ],
        "en": [
            "Where did you go? Come back 🥺",
            "Tab switched away! Did you get distracted by cat videos? 🐱",
            "Leaving so soon? We still have 15 projects left to inspect 🚀",
            "I'll be waiting right here whenever you decide to come back ⏳",
            "Don't leave me alone in the background tab, it gets lonely 👻",
            "Checking Slack? Tell your team you found their next lead developer 💼",
            "Whatever is in that tab cannot beat this portfolio ✨",
            "I'm pausing animations to save your RAM until you return 🧠"
        ]
    },
    "tab_switch_back": {
        "in": [
            "Aa gaye! Mujhe miss kiya na? 😌",
            "Wapas aa gaye! Pata tha tum mere bina nahi reh sakte 😎",
            "Welcome back! Ab jaldi se portfolio dekh ke deal finalize karo 🤝",
            "Dusri tab se bore hoke aa gaye na? Maine bola tha 😜",
            "Accha hua laut aaye! Resume download button wait kar raha tha 📄",
            "Back in action! Battery bachane ke liye animations pause kiye the ⚡",
            "Aa gaye hero! Chalo ab project demo video chalu karte hain 🎬",
            "Dekha? Maine bola tha na, mera portfolio sabse addictive hai ✨"
        ],
        "en": [
            "You're back! Knew you'd miss me 😌",
            "Welcome back! I paused all scripts to save your CPU cycles ⚡",
            "Back to business! Ready to finish reviewing that resume? 📄",
            "You couldn't stay away for long, could you? Welcome back! 😎",
            "Other tabs pale in comparison! Glad to have you back ✨",
            "Resuming interactive canvas! Let's build something great together 🚀",
            "Welcome back to headquarters! Pick up right where you left off 💡",
            "Back on track! Let's turn this visit into engineering collaboration 🤝"
        ]
    },
    "exit_intent": {
        "in": [
            "Ruko ruko! Contact section to dekh lo 🥺",
            "Cross button pe mouse? Itni jaldi mat jao, baat karo 💬",
            "Arre ja rahe ho? Bookmark to karke jao portfolio ko 🔖",
            "Close karne se pehle resume to download kar lo dost! 📄",
            "Bina hire kiye jaoge to baad me pachtaoge, pakka bolta hu 😏",
            "Ruko na! Abhi to IoT Home Automation video dekhna baki hai ⚡",
            "Ek second ruko! Contact details leke jao, baad me kaam aayegi 📱",
            "Jaate jaate GitHub repo pe ek star to dete jao boss ⭐"
        ],
        "en": [
            "Wait! Check out the contact section first 🥺",
            "Heading for exit? Bookmark this site before closing the tab 🔖",
            "Before you leave, grab the PDF resume for your talent database 📄",
            "Leaving without saying hello? Drop a message in contact form ✉️",
            "Wait up! You haven't checked out the interactive IoT prototypes yet ⚡",
            "Leaving so soon? Great software engineers don't stay available forever ⏳",
            "Take my contact info! Let's connect on LinkedIn before leaving 👔",
            "One second! Drop a star on my GitHub before heading out ⭐"
        ]
    },
    "copy": {
        "in": [
            "Copy-paste developer? Mujhse seekh lo 😜",
            "Text copy kiya? Project idea pasand aa gaya? Bindaas le jao 💡",
            "Control + C master! StackOverflow ki yaad aa gayi kya? 😂",
            "Code copy kar rahe ho? Attribution me ek star zaroor dena ⭐",
            "Copy ho gaya! Ab team me share karke bolo: Banda chahiye 💬",
            "Copy karne me kya sharam, hum sab copy-paste se engineer bane 😜",
            "Text copied to clipboard! Fast fingers, smart moves 📋",
            "Copy kiya text ab seedha offer letter me paste kar do 🤝"
        ],
        "en": [
            "Copy-paste dev? Learn from the best 😜",
            "Copied to clipboard! Sharing my portfolio with your hiring committee? 💼",
            "Ctrl+C detected! Paste it directly into a job offer letter ✉️",
            "Borrowing code snippets? Drop a credit star on my GitHub repo ⭐",
            "Copying text? Imitation is the sincerest form of developer flattery 😎",
            "StackOverflow muscle memory kicking in? We've all been there 📋",
            "Text copied! Share it with your team lead and let's build 🚀",
            "Copied! Feel free to quote my architecture solutions in your meetings 💡"
        ]
    },
    "right_click": {
        "in": [
            "Source code chura rahe ho? GitHub pe star de do ⭐",
            "Inspect element kholne ki koshish? Clean code dekh ke khush hoge 🔍",
            "Right-click karke kya dhoondh rahe ho? Zero console errors milenge boss 🟢",
            "F12 ka intezar kyu? GitHub pe direct repos open source hain 💻",
            "Source code inspection? Pure semantic HTML5 and vanilla JavaScript craft ✨",
            "Right click allowed hai! Mera code open book jaisa transparent hai 📖",
            "Console check karoge to 0 warnings milengi, guaranteed 🛡️",
            "Code quality inspect kar rahe ho? A+ rating milegi pakka 🏆"
        ],
        "en": [
            "Peeking at my source? Drop a star on GitHub ⭐",
            "Inspecting elements? Notice the zero console errors and clean DOM 🟢",
            "Right-click detected! Looking under the hood? It's pure vanilla JS power ⚡",
            "Inspecting the architecture? Everything is semantic and accessible 📐",
            "Check out that clean HTML5! No messy bloated frameworks here 🛡️",
            "Peek all you want! Clean code and optimized performance speak volumes 🔍",
            "Looking for secrets? Check the console log for custom developer greetings 💻",
            "Right-click approved! Feel free to review my clean CSS architecture 🎨"
        ]
    },
    "resize": {
        "in": [
            "Window resize kar rahe ho? Responsive design testing chal rahi hai? 📐",
            "Mobile se desktop view? Har screen size pe 100% fluid hu 📱",
            "Breakpoint test kar rahe ho? Zero layout shifts, pure flexbox power ⚡",
            "Screen resize mat karo, har size pe main cute lagta hu 😉",
            "Responsive audit pass ho gaya na? Ab hire karna banta hai 🏆",
            "Media queries tight hain boss! 320px se 4K tak perfect fit 🖥️",
            "Window stretch kar rahe ho? UI elastic jaisa smooth expand hoga 🎈",
            "Responsive check complete! Google Lighthouse 100/100 responsive score 💯"
        ],
        "en": [
            "Testing responsiveness? Flawless layout across all screen breakpoints 📐",
            "Window resized! Responsive design effortlessly adapts in real time 📱",
            "From mobile viewport to ultra-wide 4K: buttery smooth fluid layout 🖥️",
            "Checking breakpoints? Zero layout shifts, pure modern CSS architecture ⚡",
            "Resize all you want! Responsive typography and flex layouts never break 🛡️",
            "Testing mobile view? Bottom navigation bar docks neatly into place 🤖",
            "Smooth responsive transition! Engineered for any device in the world 🌐",
            "Layout recalculation complete: 100% responsive test passed with flying colors 🏆"
        ]
    },
    "dark_mode": {
        "in": [
            "Hacker vibes on 😎",
            "Dark mode lovers club! Aankhon ko sukoon aur battery ko bachat 🌙",
            "Obsidian glass theme activated! Real developers code in the dark 🖤",
            "Warm amber accents with deep dark glass: pure aesthetic perfection ✨",
            "Dark mode on! Aadhi raat tak aaram se portfolio browse karo 🦉",
            "Cyberpunk terminal energy unlocked! Ab lag raha hai hacker portfolio 💻",
            "OLED black pixels powered down, pure efficiency engaged ⚡",
            "Andhere me ujala: Max ka portfolio dark mode me aur chamkega 🌟"
        ],
        "en": [
            "Hacker mode activated 😎",
            "Dark theme engaged! Pure obsidian glass and warm amber accents 🖤",
            "Saving your retinas and battery! Dark mode aesthetics at 100% 🌙",
            "Real developers code in the dark! Welcome to the night shift 🦉",
            "Cyberpunk glow online! Clean architecture looks even sharper in the dark ✨",
            "Deep dark backgrounds, high-contrast readable typography. Perfect choice 🖥️",
            "OLED-friendly dark theme engaged! Effortless on the eyes ⚡",
            "Stealth mode active! Time to review production builds in comfort 🕶️"
        ]
    },
    "light_mode": {
        "in": [
            "Aankhein jal gayi! 🕶️",
            "Flashbang! Light mode on ho gaya, dhoop ke chashme pehno ☀️",
            "Clean paper editorial aesthetic! Day shift developers ke liye mast 📰",
            "Suraj nikal gaya portfolio me! Bright ideas and crisp typography ☀️",
            "Light mode lovers bhi exist karte hain? Swagat hai aapka 😄",
            "Crisp glass and warm amber borders: clean minimalism at its best 📄",
            "Dopahar ki dhoop jaisi freshness! Light mode ready hai boss 🌤️",
            "Brightness 100%! Ab sab kuch saaf aur clear dikh raha hai 🔍"
        ],
        "en": [
            "My eyes! Too bright 🕶️",
            "Flashbang deployed! Just kidding, crisp editorial light theme active ☀️",
            "Clean paper aesthetic loaded! Crisp contrast for bright sunny rooms 📰",
            "Sunlight mode on! High-contrast readability across every case study 🌤️",
            "Day shift mode engaged! Clean ivory glass and warm amber outlines 📄",
            "Bright and clear! Perfect for outdoor reading on mobile devices 📱",
            "Frosted white glass look engaged! Minimalist, clean, and modern ✨",
            "Light theme active! Showing off true versatility in color architecture 🎨"
        ]
    },
    "konami_code": {
        "in": [
            "Secret unlock! Ab to hire karna hi padega 🎉",
            "Up Up Down Down... Gamer spotted! Max bhi gamer hai boss 🎮",
            "Cheat code enabled! Unlimited developer productivity unlocked ⚡",
            "Konami code master! Tum pakka 90s ke legendary gamer ho 👾",
            "Secret easter egg mil gaya! Special interview call to banti hai 📞",
            "Power level over 9000! Super Saiyan developer mode activated 🔥",
            "Contra yaad aaya? 30 lives mil gayi portfolio explore karne ki 🕹️",
            "Achievement Unlocked: 'Curious Hacker'! Full respect dost 🎖️"
        ],
        "en": [
            "Secret unlocked! You've got to hire me now 🎉",
            "Konami Code entered! True gamer instincts detected 🎮",
            "Cheat code activated: Unlimited software reliability and zero bugs ⚡",
            "Up Down Left Right... You know the sacred gaming scripture! 👾",
            "Achievement unlocked: Elite Explorer! Let's build legendary games together 🕹️",
            "Secret terminal override! Unlimited engineering passion granted 🔥",
            "Retro gamer spotted! Contra 30 lives cheat code lives forever 🕹️",
            "You found the easter egg! Now let's unlock an interview 📅"
        ]
    },
    "visit_1st": {
        "in": [
            "Pehli baar aaye ho? Swagat hai! Main hu Max ka robot 🤖",
            "Welcome! Pehli nazar me portfolio pasand aayega, guarantee meri hai ✨",
            "First impression matters! Projects dekho aur batana kaisa laga 🚀",
            "Namaste! Portfolio me aapka pehla din mangalmay ho 🌸",
            "First visit! Resume, projects, aur awards sab explore karna araam se 📂",
            "Pehli baar aaye ho? Secret ye hai: Code super clean hai 💡",
            "Welcome to Mahendra Mali's digital space! Enjoy the high-performance tour 🏎️",
            "Start from About or Projects! Guidance ke liye main hu 🧭"
        ],
        "en": [
            "First time here? Welcome! I'm Max's interactive robot assistant 🤖",
            "Welcome! Take a self-guided tour through high-performance engineering builds 🚀",
            "First visit! Glad you're here to inspect my full-stack portfolio ✨",
            "Welcome aboard! Explore production projects, IoT builds, and case studies 📂",
            "First time visiting? Check out the featured IoT home automation system ⚡",
            "Great to meet you! Navigate via the bottom dock or shortcuts 🧭",
            "Welcome! Everything here is crafted with clean vanilla code and speed 💨",
            "First impressions count! Let me show you what premier software is 🌟"
        ],
        "regional": {
            "US": [
                "Welcome to the portfolio y'all! First time visiting? Enjoy the ride 🇺🇸",
                "Howdy! First visit? Check out modern systems engineering at its finest 🦅"
            ],
            "UK": [
                "Welcome! First time having a look around? Fancy a proper tour? 🫖",
                "Splendid to have you! First visit to Mahendra's engineering showroom 🇬🇧"
            ]
        }
    },
    "visit_2nd": {
        "in": [
            "Doosri baar aaye ho! Matlab portfolio sach me pasand aaya boss 😏",
            "Second visit! Hiring manager ko link share karne aaye ho na? 🔗",
            "Wapas dekhne aaye? Projects ka charm hi aisa hai dost 🚀",
            "Welcome back for round 2! Ab decision lo aur message bhejo ✉️",
            "Second time visitor! Ab hum dost ban chuke hain dost 😄",
            "Confirm karne aaye ho na doosri baar? Haan, Max best hai 🏆",
            "Round 2! Konsa project dobara dekhne aaye ho, batana zaroor 🔍",
            "Doosri baar aaye ho to seedha resume download kar lo dost 📄"
        ],
        "en": [
            "Second visit! You must really like what you saw earlier 😏",
            "Welcome back for round two! Sharing this with your tech team? 🔗",
            "Second visit confirmed! The project builds are pretty captivating, right? 🚀",
            "Round two! Time to move forward and set up an interview 📅",
            "Welcome back! You're clearly serious about finding top engineering talent 🎯",
            "Visiting again? Jump straight into the deep architecture case studies 🔍",
            "Second look! Let's turn this interest into a conversation today 💬",
            "Glad you came back! Enjoy reviewing my full technical timeline 📜"
        ]
    },
    "visit_5th": {
        "in": [
            "5th baar aaye ho, ab interview ke liye call kar do 😏",
            "5 visits ho gayi! Itna regular to koi customer nahi hota 😂",
            "Panchvi baar! Ab to bina hire kiye jana jurm mana jayega ⚖️",
            "5th visit milestone! Tum mere sabse loyal fan ban chuke ho 🎖️",
            "Abhi bhi soch rahe? 5 baar dekha, offer letter do 📜",
            "5th time! HR ko bolo interview schedule karein, delay mat karo ⏰",
            "High visit count! Dil me Max ke liye special jagah ❤️",
            "Panch baar aaye ho, coffee pe milna banta hai ab to ☕"
        ],
        "en": [
            "5th visit! Just call me for an interview already 😏",
            "5th visit milestone! You've spent serious time on my portfolio 😂",
            "Five visits deep! What questions are holding you back? Ask directly ✉️",
            "5th visit! That's true hiring intent. Let's schedule that interview call 📅",
            "Visiting 5th time? You want me on your engineering team 🎯",
            "Five visits! Let's skip small talk and discuss your open positions 💼",
            "5th time around! Bookmark is permanent, time to seal the deal 🤝",
            "High frequency visitor! Let's get down to business and build together 🚀"
        ]
    },
    "visit_10th": {
        "in": [
            "10th visit! Bhai contract paper pe sign leke hi manoge kya? 🖋️",
            "Dusvi baar! Tumhe portfolio ka har word yaad ho gaya 🧠",
            "10 visits complete! Ab seedha company ka partner bana lo mujhe 🤝",
            "Itna stalk crush ko nahi kiya hoga jitna mere portfolio ko 😂",
            "Milestone 10! Lifetime achievement award milna chahiye tumhe 🏆",
            "10th visit! Lagta hai poori company me link bhej chuke ho 🌐",
            "Dus baar dekha! Ab salary discussion ka time aa gaya 💰",
            "10th visit ho gaya! Chalo celebration me contact form submit karo 🎉"
        ],
        "en": [
            "10th visit! At this point, we're practically team members already 🖋️",
            "Double digit visits! You probably have my source code memorized now 🧠",
            "10 visits! Let's skip screening and jump straight to an offer 🤝",
            "You've visited 10 times! Dedication like this deserves an immediate email 📧",
            "Milestone reached: 10th visit! You're officially my number one visitor 🏆",
            "10 visits deep! Let's build software that scales globally together 🚀",
            "Ten visits! Officially time to talk start dates and upcoming projects 📅",
            "10th time here! Let's celebrate by scheduling an engineering interview 🎉"
        ]
    },
    "festival_diwali": {
        "in": [
            "Shubh Deepavali! 🪔 Roshni aur clean code se sab jagmagaye!",
            "Happy Diwali! Kaju katli khao aur bug-free software banao 🪔",
            "Diwali vibes! Patakhe nahi, production deployments phodo aaj 🎆",
            "Shubh Diwali! Is saal sabhi tests green rahein aur career chamke ✨",
            "Diwali ki hardik shubhkamnayein! Diye jalao aur portfolio ghoomo 🪔",
            "Diwali bonus: Max ka portfolio explore karne ka mauka mila 🎁",
            "Lakshmi ji ki kripa ho aur bug-free code ka vardaan mile! 🪔",
            "Happy Diwali! Sweet khao aur contact page pe wishes bhej do 🍬"
        ],
        "en": [
            "Happy Diwali! Wishing you brightness, prosperity, and clean code 🪔",
            "Festival of lights! May your deployments be smooth and error-free ✨",
            "Happy Diwali! Celebrating triumph of light over dark, bugs over features 🪔",
            "Warmest Diwali greetings! Let's illuminate the web with fast code 🎆",
            "Happy Diwali! May the festival of lights brighten your day 🪔",
            "Wishing you joy and success this bright Diwali season! 🪔",
            "Celebrate Diwali with sparkling ideas and high performance code ✨",
            "Joyous Diwali! Let's illuminate the web with fast software 🪔"
        ]
    },
    "festival_holi": {
        "in": [
            "Bura na mano Holi hai! 🎨 Rangeen code aur gujiya khate raho",
            "Happy Holi! Rang lagao par laptop pe paani mat daalna dost 🔫",
            "Holi vibes! UI me colorful gradients aur man me khushi rahe 🌈",
            "Rang barse! Code me colors aur portfolio me full energy 🎨",
            "Shubh Holi! Pichkari baad me, pehle portfolio enjoy karo 💦",
            "Happy Holi! Har rang ki tarah mere projects bhi diverse hain 🌈",
            "Thandai piyo, Holi khelo, aur Max ko message bhej do 🥛",
            "Holi ki shubhkamnayein! Zindagi me bugs kam aur rang zyada ho 🎨"
        ],
        "en": [
            "Happy Holi! Celebrating with vibrant colors and creative code 🎨",
            "Festival of colors! May your software architecture be just as vibrant 🌈",
            "Happy Holi! Colorful pixels, zero bugs, and endless celebration 🎉",
            "Wishing you a joyful and colorful Holi celebration today! 🎨",
            "Happy Holi! May your day be splashed with vibrant happiness 🎨",
            "Colors of spring and clean code: happy Holi celebration! 🌈",
            "Wishing you a lively, colorful and joyous Holi today 🎉",
            "Celebrate Holi with creativity, vibrant projects, and cheerful spirits 🎨"
        ]
    },
    "festival_new_year": {
        "in": [
            "Happy New Year! 🎉 Naya saal, naye projects, nayi energy!",
            "New Year resolution: Clean code likhna aur Max ko hire karna 🍾",
            "Happy New Year! 365 din, 365 commits ka target hai boss 📅",
            "Naya saal mubarak! Purane bugs bhool jao, naya code shuru karo 🚀",
            "New Year vibes! Team ko nayi unchaiyon pe le jao 🥂",
            "Happy New Year! Party baad me, goal set karo pehle 🎯",
            "Naye saal me naya developer: Mahendra Mali ready hai 🤝",
            "Cheers to a brand new year filled with speed and innovation 🥂"
        ],
        "en": [
            "Happy New Year! Here's to clean code and breakthrough innovations 🎉",
            "New Year resolution: Build faster, scale higher, hire better 🍾",
            "Happy New Year! May tests pass and servers stay up always 🚀",
            "Happy New Year! Ready to architect modern software systems together 🥂",
            "Cheers to a fresh year filled with high-impact engineering milestones 🎯",
            "New Year, new possibilities! Let's kick off with top-tier collaboration 🤝",
            "Happy New Year! Wishing you incredible growth and zero technical debt 🌟",
            "365 days of opportunities ahead! Let's build something unforgettable 🎆"
        ]
    },
    "festival_christmas": {
        "in": [
            "Merry Christmas! 🎄 Santa se maine ek solid job offer manga hai",
            "Christmas vibes! Gift me kya mila? Max ka portfolio ka link 🎁",
            "Merry Christmas! Cakes khao, enjoy karo, aur code explore karo 🎂",
            "Santa Claus is coming to town with bug-free code updates 🎅",
            "Christmas tree pe lights aur portfolio me glowing animations! Mast match 🎄",
            "Merry Christmas! Chhuttiyon me portfolio dekhne ka maza hi alag hai ❄️",
            "Santa se bolo Max ko aapki team me gift wrap karein 🎁",
            "Happy holidays! Warm coffee aur hot projects ka maza lo ☕"
        ],
        "en": [
            "Merry Christmas! Wishing you joy, peace, and bug-free production 🎄",
            "Happy Holidays! Santa brought you the gift of clean software engineering 🎁",
            "Merry Christmas! May your holidays be restful and full of warmth 🎅",
            "Season's greetings! Enjoy the holidays and check out my featured builds ❄️",
            "Merry Christmas! Best gift for your team is great engineer 🎁",
            "Holiday cheer is in the air! Hope you're enjoying festive moments 🎄",
            "Merry Christmas! Enjoy the cookies and explore full-stack case studies 🍪",
            "Wishing you a wonderful holiday season and a prosperous year ahead 🌟"
        ]
    },
    "device_mobile": {
        "in": [
            "Mobile view pe dekh rahe? Touch gestures ekdum butter smooth hain 📱",
            "Android ho ya iPhone? Bottom dock dono pe sleek chalta hai 🚀",
            "Pocket me portfolio! 144Hz high refresh rate pe enjoy karo 🏎️",
            "Mobile responsive design! Single thumb se poori site navigate hoti hai ☝️",
            "Phone pe bhi 0 lag! Mobile optimization me Max pro hai ⚡",
            "Reel format videos dekho mobile me! Fullscreen 9:16 ratio fit hai 🎬",
            "Vertical screen pe robot mascot aur bhi cute lagta hai na? 😉",
            "Mobile developer experience: Fast, lightweight, zero unnecessary bloat 📱"
        ],
        "en": [
            "Browsing on mobile? Enjoy buttery smooth thumb-friendly navigation 📱",
            "Optimized for high-refresh mobile screens! 120Hz/144Hz responsive fluid feel 🏎️",
            "Clean mobile bottom dock: Every section just a single tap away ☝️",
            "Mobile-first responsive architecture: Zero layout shifts, instant touch response ⚡",
            "Fullscreen mobile video reels formatted in native 9:16 aspect ratio 🎬",
            "High performance on any mobile chipset, whether flagship or budget 📱",
            "Pocket-sized engineering showcase! Swipe, tap, and explore with ease 🧭",
            "Engineered for mobile ergonomics from the ground up 🛠️"
        ]
    },
    "device_desktop": {
        "in": [
            "Desktop view pe welcome! Badi screen pe mera dock mast lagta 🖥️",
            "Ultrawide monitor hai kya? Multi-column layouts cleanly spread hote hain 💻",
            "Mouse aur keyboard shortcuts: Pro power-user experience enjoy karo ⌨️",
            "Desktop mode me floating robot companion hamesha aapke sath hai 🤖",
            "Dual monitor setup? Ek screen pe mera portfolio open rakhna banta 🖥️",
            "Hover effects aur tilt: Badi screen pe full detail dikhti hai ✨",
            "Desktop engineering station! Code inspect karne ka best view 🔍",
            "High resolution displays: Vector icons aur typography crystal clear hain 💎"
        ],
        "en": [
            "Browsing on desktop? Enjoy the full panoramic engineering workspace 🖥️",
            "High-DPI desktop view: Crystal-clear vector rendering and fluid layouts 💎",
            "Hover micro-interactions and smooth keyboard shortcuts enabled ⌨️",
            "Floating AI companion dock anchored neatly on your desktop screen 🤖",
            "Dual monitor developer setup? Perfect canvas for deep technical reviews 🖥️",
            "Enjoy rich ambient canvas effects and hardware-accelerated transitions ⚡",
            "Desktop ergonomics: Quick navigation drawer expands effortlessly at a glance 📂",
            "Big screen, big ideas! Let's review production architecture in full detail 🔭"
        ]
    },
    "os_mac": {
        "in": [
            "MacBook pe dekh rahe? Command Click se fast links kholo 🍏",
            "Retina display pe font rendering aur bhi buttery smooth lagti hai ✨",
            "macOS user spotted! Unix lovers ke sath meri achhi jamti hai 💻",
            "M-series silicon chip power! Mera lightweight code battery bilkul nahi khayega 🔋",
            "Trackpad gestures se scroll karo, 120Hz ProMotion pe maza aayega 🏎️",
            "Apple ecosystem aesthetics aur mera warm amber theme: perfect pair 🎨",
            "Terminal Zsh user? Mera MAXTER suite check karna mat bhoolna 🛠️",
            "MacBook touchpad se robot pe tap karo, haptic feedback feel hoga 🤖"
        ],
        "en": [
            "Viewing on macOS? Appreciate that crisp Retina typography rendering 🍏",
            "Mac user! Smooth trackpad momentum scrolling feels effortless here 🏎️",
            "Unix under the hood! Let's talk POSIX compliance and shell pipelines 💻",
            "Optimized for Apple Silicon: zero CPU throttle and light battery draw 🔋",
            "ProMotion 120Hz display? Enjoy ultra-fluid hardware accelerated animations ✨",
            "Clean macOS aesthetic meets precision software engineering 📐",
            "Power user on Mac? Try keyboard navigation and quick drawer shortcuts ⌨️",
            "macOS detected! Check out my terminal optimization toolchains 🛠️"
        ]
    },
    "os_windows": {
        "in": [
            "Windows user spotted! Alt Tab se pehle resume download kar lo 🪟",
            "DirectX hardware acceleration on! Smooth 144Hz FPS unlocked 🎮",
            "WSL use karte ho? Linux tools me mera hath saaf hai 🐧",
            "Windows PC pe bhi zero lag, pure optimized standard web standards ⚡",
            "Surface tablet ya desktop? Har screen size pe responsive fit hai 💻",
            "Taskbar me pin kar lo portfolio, baad me kaam aayega boss 📌",
            "Windows terminal me mera code clone karke run karo, smooth chalega 🚀",
            "Console check kar lo, zero errors aur bugs milenge 🛡️"
        ],
        "en": [
            "Windows detected! Running buttery smooth with hardware acceleration 🪟",
            "Power user on Windows? Check out the cross-platform engineering builds 💻",
            "WSL and Linux tooling: I bridge Windows and Linux servers easily 🐧",
            "Smooth 144Hz refresh rates supported for fluid gaming monitor browsing 🎮",
            "Windows desktop workstation: Clean layouts and responsive typography 🖥️",
            "Cross-platform compatibility tested and verified on modern Windows builds 🛡️",
            "Fast load times on Edge, Chrome, and Firefox on Windows machines ⚡",
            "Welcome Windows developer! Check out my backend and systems projects 🚀"
        ]
    },
    "os_linux": {
        "in": [
            "Linux user?! Sacha geek mil gaya! Arch, Debian, ya Ubuntu? 🐧",
            "Root permission granted! Kernel level respect for fellow Linux lovers 💻",
            "Terminal se aaye ho? sudo hire mahendra command run kar do ⚡",
            "POSIX compliant portfolio! Zero proprietary bloatware, pure FOSS spirit 🛡️",
            "Bionic libc aur Zsh customization mera forte hai, projects check karo 🐧",
            "Arch btw? I use Linux for all my production server deployments 🚀",
            "Vim user ya Neovim? Shortcut keys pasand hain to drawer dekho ⌨️",
            "Open source developer to developer connection! Star my GitHub repos ⭐"
        ],
        "en": [
            "Linux user detected! Immense respect for fellow open-source engineers 🐧",
            "sudo hire mahendra: Password accepted, engineer hired! 💻",
            "Pure POSIX philosophy: modular, lightweight, and blazingly fast ⚡",
            "Arch, Debian, or Fedora? Linux powers my entire production backend 🐧",
            "Kernel-level admiration! Check out my MAXTER terminal customization suite 🛠️",
            "FOSS spirit runs deep: clean vanilla code with zero tracking bloat 🛡️",
            "Vim keybindings enthusiast? Everything here is built with precision ⌨️",
            "Greetings fellow Linux developer! Let's build robust decentralized systems 🚀"
        ]
    },
    "welcome_back": {
        "in": [
            "Wapas aa gaye! Miss kiya 🤗",
            "Aapka phir se swagat hai! Naye updates dekhne aaye ho na? ✨",
            "Returning visitor! Aapke liye robot antenna hamesha active rehta hai 📡",
            "Wapas dekh ke khushi hui! Chalo conversation ko aage badhate hain 💬",
            "Second innings shuru! Is baar bina message kiye mat jana dost 🤝",
            "Aap laut aaye! Browser me fast cache save kar rakha tha ⚡",
            "Welcome back! Kya resume forward ho gaya engineering team ko? 📄",
            "Dil me bas gaye lagta hai! Wapas aane ke liye shukriya ❤️"
        ],
        "en": [
            "Welcome back! Missed you 🤗",
            "Great to see you again! Checking out latest project additions? ✨",
            "Returning visitor detected! My circuits light up whenever you return 💡",
            "Welcome back! Ready to advance to an introductory engineering interview? 📅",
            "Glad you returned! Pick up right where you left off 🔍",
            "Cached and ready! Instant page loads for our loyal returning guests ⚡",
            "Back again? Let's turn this sustained interest into an active build 🚀",
            "Welcome back aboard! Let me know if you need any details 📬"
        ]
    },
    "resume_download": {
        "in": [
            "Download ho gaya? Ab mail bhi kar do, main wait kar raha hu 📧",
            "Resume downloaded! Vector PDF ready hai HR meeting ke liye 📄",
            "Shabash! Resume download ho gaya, ab interview date decide karein 📅",
            "PDF saved! Zero fluff, pure engineering achievements inside 💼",
            "Resume download complete! Forward it to the engineering director 🚀",
            "Download done! Print nikal ke signing table pe rakh do boss 🖋️",
            "Ek resume download se aapki team ka technical debt zero hoga ⚡",
            "Resume download ho gaya! Ab email send karne ka countdown shuru ⏳"
        ],
        "en": [
            "Resume downloaded! Now drop me an email, I'm waiting 📧",
            "Vector CV downloaded! Ready for your engineering hiring review 📄",
            "Download complete! Forward my credentials to the engineering leadership team 💼",
            "Resume secured! Take your time reviewing my achievements and impact 📈",
            "Saved to your device! Reach out directly when ready to talk 📞",
            "Download successful! Let's follow up with a quick introductory call 📅",
            "CV downloaded! Packed with verified systems impact and project milestones 🏆",
            "Got the resume? Shoot me a message to discuss open roles 🤝"
        ]
    },
    "cursor_on_robot": {
        "in": [
            "Hehe, gudgudi ho rahi hai! 😆",
            "Cursor mere upar? Dosti karoge kya mere se? 🤖",
            "Hover kiya to dil khush ho gaya! Click bhi karke dekho ✨",
            "Tickle tickle! Mere sensors bhot sensitive hain dost 😄",
            "Aapka cursor kitna gentle hai! Mujhse baat karna chahte ho? 💬",
            "Aankhon me dekh rahe ho? Blushing cheeks activaed ho gaye 🌸",
            "Robot ko pat kar rahe? Good human! Main aapko pasand karta 💙",
            "Cursor hovering on robot: AI companion is delighted to meet you 🦾"
        ],
        "en": [
            "Hehe, that tickles! 😆",
            "Hovering over me? Care to tap and explore the quick menu? 🤖",
            "Tickle detected! My sensor arrays are humming with delight ✨",
            "Direct cursor contact! Look at my rosy blushing cheeks 🌸",
            "You found the mascot! Click me to open the navigation deck 📂",
            "Hovering close! Are you admiring my sleek cybernetic visor? 😎",
            "Virtual head pat received! You're an awesome visitor, friend 💙",
            "Friendly robot at your service! Where would you like to go? 🧭"
        ]
    },
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

def validate_captions():
    total_triggers = len(CAPTIONS_DATA)
    total_captions = 0
    issues = []
    dash_regex = re.compile(r'[\u2013\u2014]')
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

    js_content = "/* Auto-generated robot captions dataset - Zero em/en-dashes */\n"
    js_content += "window.MAXHIVE_CAPTIONS = " + json.dumps(CAPTIONS_DATA, indent=2, ensure_ascii=False) + ";\n"
    with open("js/captions.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Exported to js/captions.js successfully!")

if __name__ == "__main__":
    validate_captions()
