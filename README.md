# AI Personal Trainer Starter

**English** | [Русская версия](README.ru.md)

A beginner-friendly project for learning how to use AI to organize workouts, goals, schedules, and progress notes with simple text files.

> **Start here:** this public repository is a starter/learning project. You can use it three ways: **(1) make a public fork for experimenting or contributing, (2) make a separate private GitHub copy for personal use, or (3) keep everything in a local folder on your own computer with no GitHub repository at all.** Never put real personal, medical, school, contact, or health information in a public fork or public repository.

This guide is written for people who are new to AI, GitHub, and software development. You do **not** need to be a programmer.

---

## What this project does

The idea is simple:

1. Your information is stored in easy-to-read Markdown files (`.md` files).
2. GitHub keeps those files organized and saves a history of changes.
3. An AI assistant can read the files, help create a plan, update logs, and explain what changed.
4. Planned workouts stay separate from completed workouts so the AI does not accidentally pretend something happened when it did not.

Think of it as a smart training notebook with a very organized filing system.

This is a learning and organization tool. It is **not a doctor, physical therapist, dietitian, or emergency service**.

---

# Choose how you want to use this project

There is no single required setup. Pick the option that fits what you are doing.

## Option 1 — Public fork

A **fork** is your own GitHub copy that stays connected to this public starter.

Use a fork when you want to:

- experiment with the public project
- suggest improvements
- learn GitHub
- keep your work connected to the original project

**Important:** a fork of this public repository is also public. Do **not** put personal training records, health information, school information, addresses, private contact information, passwords, or API keys in the fork.

This option is best for **sample/demo data and project contributions**, not a real person's private training record.

## Option 2 — Separate private GitHub copy

This is a good choice when you want:

- private storage
- GitHub's change history
- access from more than one computer
- easy backup/sync through GitHub
- Codex to work with the repository through GitHub

This copy should be a **new private repository, not a public fork**.

## Option 3 — Local folder only (no GitHub)

This is the simplest option if you want the files to live only on your computer.

You can:

1. Download the starter as a ZIP file.
2. Unzip it into a normal folder such as `Documents/AI-Personal-Trainer`.
3. Open that folder as a local project in a Codex-capable desktop/CLI/IDE workflow.
4. Let the AI read and edit the Markdown files in that folder.
5. Back up the folder yourself.

You do **not** need a GitHub account, GitHub repository, web hosting, database, or domain for this option.

The tradeoff is that GitHub will not automatically provide remote backup or web-based version history. You are responsible for backups. You can optionally use local Git later without ever publishing the folder to GitHub.

## Which option should I choose?

| Setup | Good for | Personal/private data? | GitHub required? |
|---|---|---:|---:|
| **Public fork** | Learning, demos, contributing back | **No** | Yes |
| **Separate private GitHub copy** | Personal use with sync/history | Yes | Yes |
| **Local folder only** | Personal use on one computer, simplest storage | Yes, if the computer is appropriately protected | **No** |

For kids, a parent, guardian, teacher, or coach should help decide which option is appropriate and what information should be saved.

---

# What do I need?

You can start with **$0**.

| Item | Required? | Free option? | What it is |
|---|---|---:|---|
| Web browser | Yes | Yes | Chrome, Safari, Edge, Firefox, etc. |
| GitHub account | Only for the fork or GitHub-copy options | Yes | Stores/syncs project files online |
| Private GitHub repository | Only for the private GitHub option | Yes | Keeps a personal GitHub copy private |
| ChatGPT account | Yes for the AI workflow | Yes | Gives you access to ChatGPT and limited Codex usage |
| Codex | Recommended | Included with ChatGPT plans, with limits that vary by plan | AI tool that can work on repository files |
| GitHub Copilot | No | Optional | Not required for this project |
| OpenAI API key | No | No need to buy API usage | Not required for the beginner setup |
| Git, terminal, or command line | No for the browser/GitHub path; optional for local use | — | Local Git/Codex CLI is optional, not required by the project itself |
| VS Code or another code editor | No | — | Optional; a local Codex/IDE workflow can use a normal folder |
| Website hosting/domain | No | — | This project does not need to be deployed as a website |

### Free vs. paid

If you choose a GitHub-based setup, **GitHub Free is enough** for this project and includes private repositories. If you choose the local-folder setup, you do not need GitHub at all.

**ChatGPT Free can be used to get started with Codex**, but usage is limited. Paid ChatGPT plans are optional and mainly provide more usage and features.

You do **not** need to buy GitHub Pro, GitHub Copilot, an OpenAI API key, hosting, a database, or a custom domain to get started.

Pricing and plan limits can change. Before paying for anything, check the official pages:

- GitHub pricing: https://github.com/pricing
- ChatGPT pricing: https://chatgpt.com/pricing/
- Codex with ChatGPT plans: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan

**Last pricing/feature check for this README: September 22, 2026.**

---

# Important age rules for a kids' project

Please read this before creating accounts.

- GitHub requires users to be at least **13 years old**. Some countries may require a higher minimum age.
- OpenAI requires users to be at least **13 years old or the minimum age required in their country**. Users under 18 need permission from a parent or legal guardian.
- If a child is below the minimum age for a service, do not create an account for the child or share an adult password with them. An adult or school should operate the service in a way that follows the service's rules.
- Schools may have their own technology, privacy, and parental-consent requirements.

Official terms:

- GitHub Terms: https://docs.github.com/en/site-policy/github-terms/github-terms-of-service
- OpenAI Terms: https://openai.com/policies/terms-of-use/

---

# Beginner vocabulary

You only need a few words.

### Repository (repo)

A repository is a project folder stored on GitHub.

### Public repository

Anyone on the internet can view it. Use public repositories only for examples, instructions, and information you are comfortable sharing publicly.

### Private repository

Only you and people you explicitly allow can see it. **Use a private repository for real personal training data.**

### Markdown

Markdown is ordinary text with simple formatting. Files usually end in `.md`.

Example:

```md
# My Goal

I want to improve my 1-mile run while training three days per week.
```

### Commit

A commit is a saved checkpoint. It lets you see what changed and, if needed, return to an earlier version.

### AI prompt

A prompt is simply the instruction or question you give the AI.

### AGENTS.md

This is a special instruction file that tells an AI agent how it should behave while working in the repository.

You can think of it as the project's rulebook.

---

# Beginner setup

Choose **one** of the three paths below. You can switch later.

## Path A — Make a public fork

Use this only for public examples, experiments, or contributing improvements back to the starter.

1. Create or sign in to a GitHub account at https://github.com/signup
2. Open this public starter repository.
3. Click **Fork**.
4. Create the fork under your GitHub account.
5. Keep only sample/demo information in it.
6. Never add real personal, health, school, address, account, or other sensitive information.

Because the original repository is public, the fork is public too.

---

## Path B — Make a separate private GitHub copy

Use this when you want personal files stored privately on GitHub.

### Step B1 — Create a GitHub account

1. Go to https://github.com/signup
2. Create an account.
3. Verify your email address.
4. You can stay on the free plan.
5. Turn on two-factor authentication if GitHub asks you to do so.

You do not need a paid GitHub plan for this project.

### Step B2 — Create the private copy

**Do not use a public fork for personal information.**

If this starter has a **Use this template** button and GitHub lets you create a private repository from it:

1. Click **Use this template**.
2. Choose **Create a new repository**.
3. Give it a simple name such as:
   - `my-training-workspace`
   - `fitness-project`
   - `training-notebook`
4. Choose **Private**.
5. Create the repository.

If you do not see that option:

1. On this public starter repository, click **Code**.
2. Choose **Download ZIP**.
3. Unzip the downloaded file.
4. Go to https://github.com/new
5. Create a new repository.
6. Select **Private**.
7. In the new repository, choose **Add file → Upload files**.
8. Upload the starter files.
9. Save/commit the upload.

This private repository is a separate copy. It is not connected to the public repository as a fork.

---

## Path C — Use a local folder only (no GitHub)

Use this when you want the project to live in ordinary file-system space on your computer.

### Step C1 — Download the starter

1. On this public repository, click **Code**.
2. Choose **Download ZIP**.
3. Find the ZIP file in your Downloads folder.
4. Unzip/extract it.
5. Move the extracted folder somewhere easy to find, for example:
   - Windows: `Documents\\AI-Personal-Trainer`
   - macOS: `Documents/AI-Personal-Trainer`
6. Rename the folder if you want.

At this point, the project is just a normal folder containing normal text files.

### Step C2 — Make a backup plan

Without GitHub, you are responsible for backups.

A simple backup can be:

- a second copy on an external drive
- a computer backup system
- a private cloud-storage folder that your parent/guardian, school, or organization approves

Be careful with shared cloud folders. A local project can still become visible to other people if you save it inside a shared drive.

### Step C3 — Let Codex work with the local folder

For direct local-file editing, use a Codex workflow that can open a folder on your computer, such as the ChatGPT desktop/Codex local-project experience, Codex CLI, or a supported IDE integration.

The basic idea is:

1. Open the local project folder.
2. Start Codex in that folder/project.
3. Ask it to read `README.md` and `AGENTS.md`.
4. Give it the setup prompt later in this guide.
5. Review file changes before accepting them.

You do **not** have to publish the folder to GitHub.

OpenAI's current Codex CLI/local-project documentation:
https://developers.openai.com/codex/cli

---

## Step 3 — Create or sign in to ChatGPT

1. Go to https://chatgpt.com/
2. Sign in or create an account.
3. The free plan is enough to begin.
4. Paid plans are optional.

You do not need an OpenAI API key for the beginner workflow.

---

## Step 4 — Open Codex

Codex is the part of OpenAI's tools designed to work with project files.

### If you chose the GitHub path

1. Sign in with the same ChatGPT account.
2. Open **Codex**.
3. Choose the option to connect or work with GitHub.
4. GitHub may ask you to authorize the OpenAI/ChatGPT GitHub app.
5. For a private personal project, give it access to **only the private training repository you created**, unless you have a reason to share more.
6. Select the correct repository.

If the repository does not appear immediately, check that the GitHub app has permission to access it.

OpenAI's GitHub connection guide:

https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt

### If you chose the local-folder path

Open the folder as a local project using a supported Codex desktop, CLI, or IDE workflow. Codex can then inspect and edit files in that local project without requiring the project to be hosted on GitHub.

OpenAI's Codex CLI guide:

https://developers.openai.com/codex/cli

### Important: ChatGPT web vs. a local project

A normal ChatGPT web project does not automatically gain access to arbitrary folders on your computer. For a filesystem-only setup, use a local Codex-capable workflow or manually upload the files you want ChatGPT to read.

---

# Step 5 — Give the AI its first setup job

If your private GitHub copy or local folder does not already contain starter folders, paste the following into Codex.

```text
I am setting up a private AI-assisted personal training workspace.

Please create a simple beginner-friendly structure using Markdown files.

Create:
- AGENTS.md
- profile/goals.md
- profile/availability.md
- profile/training-preferences.md
- profile/equipment.md
- profile/constraints.md
- schedule/current.md
- templates/workouts/
- logs/workouts/
- logs/check-ins/
- research/

Rules:
1. Keep planned workouts separate from completed workout logs.
2. Never invent a completed workout, measurement, symptom, meal, or result.
3. Ask before making a major change to an adopted plan.
4. Use plain English.
5. Explain every file you create or change.
6. Do not add private information I did not explicitly provide.
7. Do not store passwords, API keys, addresses, school information, or account credentials.
8. If the athlete is a minor, favor age-appropriate training, skill, consistency, enjoyment, recovery, and adult supervision.
9. Do not create weight-loss, restrictive-diet, supplement, or medical-treatment plans for a minor.
10. If pain, injury, illness, or another medical concern comes up, flag it for a parent/guardian and appropriate healthcare professional instead of treating it like a normal training problem.

Before making the first training plan, ask me for the minimum information you need about:
- age range
- training goal
- experience level
- days available
- time available per session
- equipment available
- sports/activities already being done
- injuries or limitations I choose to share
- anything a parent, guardian, coach, or clinician has said to avoid

Do not ask for unnecessary identifying information.
```

Review what the AI proposes before accepting the changes.

---

# Step 6 — Fill in the profile

The AI should help you fill out a few simple files.

A beginner profile might look like this:

```md
# Goals

- Improve general fitness
- Run one mile without stopping
- Learn good squat, push-up, and plank technique
- Train 3 days per week
```

An equipment file might look like:

```md
# Equipment

Available:
- Open floor space
- Resistance bands
- Light dumbbells
- Treadmill

Not available:
- Barbell
- Sled
- Rowing machine
```

A schedule file might say:

```md
# Current Schedule

Monday: 30-minute beginner strength session
Wednesday: 25-minute easy cardio + mobility
Saturday: 35-minute mixed fitness session
```

You do not have to write these files yourself. You can tell the AI the facts in normal language and ask it to put them in the correct files.

---

# A simple folder system

A good beginner version looks like this:

```text
my-training-workspace/
├── README.md
├── AGENTS.md
├── profile/
│   ├── goals.md
│   ├── availability.md
│   ├── training-preferences.md
│   ├── equipment.md
│   └── constraints.md
├── schedule/
│   └── current.md
├── templates/
│   └── workouts/
├── logs/
│   ├── workouts/
│   └── check-ins/
└── research/
```

### What each folder means

- `profile/` — slow-changing facts about goals, schedule, preferences, equipment, and limits.
- `schedule/` — what is currently planned.
- `templates/` — reusable workout ideas.
- `logs/workouts/` — what actually happened.
- `logs/check-ins/` — simple notes such as energy, soreness, sleep quality, or how a session felt.
- `research/` — useful articles, rules, or AI research notes that may influence future plans.
- `AGENTS.md` — rules the AI should follow.

The big idea is:

> **Plan = what should happen. Log = what actually happened. Never silently mix them.**

---

# How to use it day to day

You can talk to the AI normally.

## Before a workout

```text
Read my current schedule and profile. What is today's workout?
Explain it like I am a beginner.
Do not change the plan unless I ask.
```

## If equipment is unavailable

```text
The treadmill is unavailable today.
Check my equipment file and suggest a safe substitute for today's cardio.
Do not rewrite the whole weekly plan.
```

## After a workout

```text
I completed today's workout.

Actual:
- 5-minute warm-up
- 3 rounds of 8 goblet squats
- 3 rounds of 6 incline push-ups
- 3 x 20-second planks
- 10 minutes easy walking

Difficulty: 5/10
No pain.

Please create today's workout log.
Do not change the original plan to make it look like I completed something different.
```

## If the workout was only partly completed

```text
I stopped after the second round because I ran out of time.
Log exactly what I completed.
Do not mark the unfinished work as complete.
```

## Weekly review

```text
Review this week's planned workouts and actual workout logs.
Show:
- what was planned
- what was completed
- what was skipped or changed
- what felt easy or difficult
- any pattern worth discussing

Do not change next week's plan yet.
Give me proposed changes separately so I can approve them first.
```

---

# How to review AI changes

AI can make mistakes.

Before accepting important changes:

1. Read the AI's summary.
2. Open the changed file.
3. Make sure it did not invent a workout, result, symptom, or personal fact.
4. Make sure planned work did not get rewritten as completed work.
5. Make sure no secret or identifying information was added.
6. For training changes, ask: "Why did you change this?"
7. If something looks wrong, tell the AI to correct it before saving.

You do not have to understand code. Most of this project is plain text.

---

# Rules for kids and teens

For minors, the project should emphasize:

- learning movement skills
- consistency
- enjoyment
- sport performance
- sleep and recovery habits
- hydration
- regular balanced meals
- age-appropriate training
- adult supervision

For minors, this project should **not** be used to independently run:

- aggressive weight loss
- calorie restriction
- "cutting"
- dehydration
- weight-class manipulation
- supplement stacks
- maximal lifting programs without qualified supervision
- training through pain or injury
- medical treatment

A parent/guardian, coach, teacher, athletic trainer, pediatric clinician, or other qualified professional should be involved when appropriate.

---

# Privacy checklist

Before saving a file, ask:

- Does this contain a password or API key? **Do not save it.**
- Does this contain a home address or school address? **Do not save it.**
- Does this contain a phone number or private email? Usually **do not save it.**
- Does this contain a child's full legal name or date of birth? Avoid it unless truly necessary.
- Does this contain medical information? Keep it private and share only what is necessary.
- If I am using GitHub, is the personal repository definitely **Private**?
- If I am using a local folder, is the computer/user account appropriately protected and backed up?
- Am I comfortable with every person who can access this repository, folder, device, or backup seeing this information?

A useful project does not need a large amount of personal information.

---

# Parent/teacher setup recommendation

For a classroom, club, family, or youth program:

1. Keep the public starter repository free of student information.
2. Use private repositories or appropriately protected local folders for any individual information.
3. Use initials, nicknames, or non-identifying labels when possible.
4. Do not publish health information.
5. Do not ask students to create accounts if they do not meet the service's age requirements.
6. Follow school/district rules for AI, student privacy, accounts, and parental consent.
7. Use sample/demo data when teaching the workflow publicly.
8. Have an adult review AI-created training plans before a child follows them.
9. Avoid body-weight or dieting projects as a default classroom activity.
10. Teach students to verify AI output rather than assuming it is correct.

---

# What if I want to track nutrition?

For an adult personal project, nutrition files can be added later.

For a kids/teen project, keep nutrition focused on healthy habits unless a qualified professional and parent/guardian are involved.

A beginner youth project usually does **not** need calorie, macro, body-fat, or weight-loss tracking.

---

# What if I want to add health information?

Health information is sensitive.

The simplest beginner approach is to keep medical records out of this project.

If an adult chooses to store health-related notes:

- use a private repository or appropriately protected local folder
- include only what is necessary
- do not publish it
- do not treat AI output as medical diagnosis or treatment
- involve an appropriate healthcare professional for pain, injury, illness, medications, or other medical concerns

---

# Common problems

## "I cannot see my repository in Codex or ChatGPT"

Check:

1. You are signed into the correct GitHub account.
2. The OpenAI/ChatGPT GitHub app has permission to access the private repository.
3. You selected the correct repository during authorization.
4. Wait a few minutes after creating or authorizing a new repository.

---

## "ChatGPT can read the files but cannot change them"

You may be using the normal GitHub connection in ChatGPT.

That connection is primarily for reading/analyzing repository content.

Use **Codex** when you want the AI to create, edit, and push repository files.

---

## "I hit an AI usage limit"

That can happen on the free plan.

You can:

- wait for the usage limit to reset, or
- optionally upgrade to a paid ChatGPT plan for more usage

Do not buy an API key just because you hit a beginner-plan limit.

---

## "The AI changed too much"

Say:

```text
Stop making broad changes.
Show me exactly which files you want to change and why.
Do not modify anything else.
```

You can also ask it to restore a previous version using Git history.

---

## "The AI says I completed something I did not do"

Correct it immediately:

```text
That was planned, not completed.
Remove it from the actual log.
Never infer completion from a schedule or template.
```

Then make sure `AGENTS.md` includes a rule that completed activity must come from an explicit user report or a trusted record.

---

## "I accidentally put private information in a public repository"

Treat it as potentially exposed.

1. Tell a parent/guardian, teacher, project owner, or administrator if appropriate.
2. Make the repository private immediately if you control it.
3. Remove the information.
4. Remember that Git history may still contain earlier versions.
5. If you exposed a password, token, or API key, change/revoke it immediately.
6. Get help from someone who understands GitHub history if the information was sensitive.

---

# Do I need to learn programming?

No.

You can use this project almost entirely by:

- clicking in a web browser
- writing normal-language prompts
- reading Markdown files
- reviewing AI changes

Learning a little GitHub vocabulary is useful, but you do not need to become a software engineer.

---

# Do I need GitHub Copilot?

No.

GitHub Copilot is a separate AI coding product. It can be useful for programmers, but this project does not require it.

---

# Do I need an OpenAI API key?

No.

For the recommended beginner setup, sign in to Codex with your ChatGPT account.

Using an API key is an advanced option with separate usage-based billing. Beginners should skip it unless they specifically want to build software around the API.

---

# Do I need to install anything?

It depends on the path you choose.

- **Public fork or private GitHub copy:** you can do the repository setup in a browser.
- **Local folder only:** the files themselves need no special software, but for AI to directly inspect and edit that folder you need a local Codex-capable workflow such as the desktop app, Codex CLI, or a supported IDE integration.
- **Manual use:** Markdown files can also be opened in ordinary text editors.

Git, VS Code, and GitHub Copilot are optional. You do not need to turn the project into a website or install a database.

---

# A good first-week learning path

### Day 1
Choose your setup: public demo fork, private GitHub copy, or local folder. Then open that project in Codex.

### Day 2
Fill in goals, availability, equipment, and preferences.

### Day 3
Ask the AI to create a simple one-week plan.

### Day 4
Complete a workout and log only what actually happened.

### Day 5
Ask the AI to explain the difference between the schedule, template, and log.

### Weekend
Review the week and ask the AI for proposed improvements without changing the next plan automatically.

The goal is not to make the AI "run everything." The goal is to learn how to give it good information, inspect its work, and keep clean records.

---

# Recommended AI rules

Your `AGENTS.md` should eventually include rules like these:

1. Never invent completed activity.
2. Keep plans separate from actual logs.
3. Ask before major plan changes.
4. Explain important changes in plain English.
5. Use the user's actual equipment and schedule.
6. Do not silently overwrite old logs.
7. Keep personal information private.
8. Flag pain, injury, illness, or other health concerns.
9. For minors, avoid restrictive dieting, unsafe loading, and unsupervised maximal training.
10. Treat AI suggestions as suggestions that a human reviews.

---

# Keeping your personal copy updated

A separate private repository or local-folder copy will not automatically receive future starter improvements. A public fork stays connected to the original project, but remember that the fork remains public.

A safe update process is:

1. Check the public starter for new instructions or example files.
2. Ask Codex to compare the public starter with your private repository or local folder.
3. Tell it **not to overwrite your profile, schedules, or logs**.
4. Review proposed framework/instruction updates.
5. Accept only the changes you understand and want.

Example prompt:

```text
Compare the current public starter structure with my private training workspace.
Propose useful framework or instruction updates only.
Do not copy personal example data.
Do not overwrite my profile, schedule, logs, or completed records.
Show me the proposed changes before applying them.
```

---

# Official help links

- GitHub signup: https://github.com/signup
- Create a GitHub repository: https://github.com/new
- GitHub pricing: https://github.com/pricing
- GitHub repository basics: https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories
- GitHub Terms: https://docs.github.com/en/site-policy/github-terms/github-terms-of-service
- ChatGPT: https://chatgpt.com/
- ChatGPT pricing: https://chatgpt.com/pricing/
- Codex with a ChatGPT plan: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- Connect GitHub to ChatGPT: https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt
- Codex CLI / local projects: https://developers.openai.com/codex/cli
- OpenAI Terms: https://openai.com/policies/terms-of-use/

---

# Final reminder

You do not need to understand AI deeply to use this project well.

Remember four things:

1. **Keep personal work private.**
2. **Tell the AI facts; do not let it invent them.**
3. **Keep plans separate from what actually happened.**
4. **Have a human review important training, health, and safety decisions.**

If you can use a shared folder, write a message, and read a checklist, you can learn this workflow.
