# WRGPT Bot Development Guide

## Project Overview
This is a WRGPT email poker tournament automation tool. Development follows a strict **Plan → Document → Execute** approach with NO over-engineering.

## Development Philosophy
- **KISS Principle**: Keep it simple, stupid
- **Plan First**: Document everything before writing code
- **Step-by-Step**: Execute one small piece at a time
- **Validate Early**: Test each phase completely before moving forward

## Current Phase: BASE MODEL VALIDATION

### Objective
Verify that the terminal-based bot can successfully:
1. Fetch the most recent dealer email
2. Display table status
3. Display current hand
4. Send action commands (call/fold/raise) back to dealer

### Before Writing ANY Code
Create a detailed plan document (`PLAN.md`) that includes:
- Email fetching strategy (IMAP/Gmail API/etc)
- Email parsing approach (regex/Beautiful Soup/etc)
- Command structure for user actions
- Exact flow from start to finish
- Error handling scenarios
- Testing checklist

### Success Criteria
- [ ] Can authenticate with email
- [ ] Can fetch most recent dealer email
- [ ] Can parse and display table status
- [ ] Can parse and display hole cards
- [ ] Can send valid action commands
- [ ] All actions work in a real WRGPT game

**DO NOT PROCEED TO ENHANCED MODEL UNTIL ALL CRITERIA MET**

---

## Phase 2: ENHANCED MODEL (Not Yet Started)

### Objective
Add web UI and probability analysis WITHOUT breaking base functionality.

### Requirements
- Web UI for base model features
- Integration with holdem-sim for probability analysis
- Must maintain all base model functionality

### Before Starting This Phase
- Complete base model validation
- Create detailed plan in `PLAN-ENHANCED.md`
- Design UI mockups/wireframes
- Document holdem-sim integration approach

---

## Phase 3: AI MODEL (Not Yet Started)

### Objective
Add AI-powered player analysis and action recommendations.

### Requirements
- Ollama integration for local AI
- Player tendency tracking
- Action recommendations based on AI analysis
- Must maintain all previous functionality

### Before Starting This Phase
- Complete enhanced model validation
- Create detailed plan in `PLAN-AI.md`
- Research Ollama integration patterns
- Design data structures for player tracking

---

## Development Rules

### Planning Phase (REQUIRED before coding)
1. Write detailed plan document for current phase
2. Break down into smallest possible steps
3. Identify all dependencies and tools needed
4. Create testing checklist
5. Get plan reviewed/approved before proceeding

### Execution Phase
1. Work on ONE step at a time
2. Test each step before moving to next
3. Commit working code frequently
4. Update plan with any deviations
5. If something seems complex, STOP and re-plan

### Anti-Patterns to AVOID
- ❌ Starting to code without a detailed plan
- ❌ Adding "nice to have" features mid-phase
- ❌ Over-abstracting with classes/inheritance
- ❌ Adding frameworks/libraries unnecessarily
- ❌ Moving to next phase without validation
- ❌ Clever/complex solutions when simple ones work

### Patterns to EMBRACE
- ✅ Simple procedural code first
- ✅ Hard-coded values during testing
- ✅ Print statements for debugging
- ✅ Single-file scripts until proven necessary to split
- ✅ Standard library over external dependencies
- ✅ Working code > elegant code

---

## Current Status
**Phase**: Base Model - Planning Stage
**Next Action**: Create `PLAN.md` with detailed base model implementation plan

## Questions to Answer Before Coding Base Model
1. What email service is WRGPT using?
2. What format are dealer emails in?
3. What authentication method should we use?
4. What information is in table status emails?
5. How do we send action emails back?
6. What's the exact email format for actions?

---

## Communication Preferences
- Ask clarifying questions BEFORE implementing
- Show plan for review BEFORE executing
- Break large tasks into reviewable chunks
- Flag any assumptions being made
- Suggest simple solutions over complex ones

## Success Metrics
- ✅ Code works on first try (because we planned)
- ✅ No unused code or dependencies
- ✅ Each phase fully validated before next
- ✅ Easy to understand and modify
- ✅ Solves the actual problem (not imagined future problems)