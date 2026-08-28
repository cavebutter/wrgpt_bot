# BASE MODEL TEST PLAN

## Overview
This test plan validates the existing base model implementation with the new email provider. Testing is split into two phases based on what can be tested before the tournament starts.

## Environment Setup Requirements

### .env File Configuration
Before any testing, ensure `.env` file contains:
```
user=<your_email_address>
password=<your_email_password>
smtp_server=<smtp_server_address>
imap_server=<imap_server_address>
smtp_port=<smtp_port_number>
id=<your_wrgpt_player_id>
dealer=<dealer_email_address>
logfile_dir=<path_to_log_directory>
```

### Dependencies
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### System Requirements
- w3m terminal browser installed (for table status display)
- Access to previous tournament emails in email account

---

## PHASE 1: Email Connectivity & Parsing
**Can be tested NOW with archived tournament emails**

### Test 1.1: Email Authentication
**Objective**: Verify connection to new email provider via IMAP and SMTP

**Test Steps**:
1. Run a simple IMAP connection test
2. Verify SMTP authentication works

**Test Script** (create `test_auth.py`):
```python
from mail_functions import Account
import os
from dotenv import load_dotenv

load_dotenv()
imap_server = os.getenv("imap_server")
user = os.getenv("user")
password = os.getenv("password")

try:
    with Account(imap_server, user, password).login() as mb:
        print("✓ IMAP authentication successful")
        print(f"  Connected to: {imap_server}")
        print(f"  User: {user}")
except Exception as e:
    print(f"✗ IMAP authentication failed: {e}")
```

**Success Criteria**:
- [ ] IMAP connection succeeds
- [ ] No authentication errors
- [ ] Can access mailbox folders

**Troubleshooting**:
- Verify IMAP is enabled on email provider
- Check if app-specific password is needed
- Verify server address and port are correct

---

### Test 1.2: Email Folder Access
**Objective**: Verify archived emails are accessible in expected folder

**Test Steps**:
1. List all available folders
2. Verify "INBOX.Poker" folder exists or identify correct folder name
3. Count emails in poker folder

**Test Script** (create `test_folders.py`):
```python
from mail_functions import Account
import os
from dotenv import load_dotenv

load_dotenv()
imap_server = os.getenv("imap_server")
user = os.getenv("user")
password = os.getenv("password")

try:
    with Account(imap_server, user, password).login() as mb:
        print("Available folders:")
        for folder in mb.folder.list():
            print(f"  - {folder.name}")

        # Try to access poker folder
        mb.folder.set("INBOX.Poker")
        count = 0
        for msg in mb.fetch():
            count += 1
        print(f"\n✓ Found {count} emails in INBOX.Poker")
except Exception as e:
    print(f"✗ Folder access failed: {e}")
    print("\nTry updating mail_functions.py if folder name is different")
```

**Success Criteria**:
- [ ] Can list all folders
- [ ] Poker folder exists (or correct folder identified)
- [ ] Can access archived tournament emails

**Notes**:
- Folder name may differ with new provider (e.g., "INBOX/Poker", "Poker", etc.)
- Update `folder` parameter in mail_functions.py if needed

---

### Test 1.3: Fetch Most Recent Email
**Objective**: Verify `fetch_most_recent()` correctly retrieves newest email

**Test Steps**:
1. Run fetch_most_recent()
2. Display email metadata
3. Verify it's actually the most recent

**Test Script** (create `test_fetch.py`):
```python
from mail_functions import fetch_most_recent
import os
from dotenv import load_dotenv

load_dotenv()
imap_server = os.getenv("imap_server")
user = os.getenv("user")
password = os.getenv("password")

try:
    recent = fetch_most_recent(imap_server, user, password)
    print("✓ Most recent email fetched:")
    print(f"  UID: {recent.uid}")
    print(f"  Subject: {recent.subject}")
    print(f"  From: {recent.from_}")
    print(f"  Date: {recent.date_str}")
    print(f"\n  Message preview:")
    print(f"  {recent.text[:200]}...")
except Exception as e:
    print(f"✗ Fetch failed: {e}")
```

**Success Criteria**:
- [ ] Function executes without errors
- [ ] Returns a Mail object
- [ ] Email is actually the most recent one
- [ ] All fields populated correctly

---

### Test 1.4: Parse Table URL
**Objective**: Verify `get_table_url()` extracts URL from dealer email

**Test Steps**:
1. Fetch most recent email
2. Extract table URL
3. Verify URL format is valid

**Test Script** (create `test_url_parse.py`):
```python
from mail_functions import fetch_most_recent, get_table_url
import os
from dotenv import load_dotenv

load_dotenv()
imap_server = os.getenv("imap_server")
user = os.getenv("user")
password = os.getenv("password")

try:
    recent = fetch_most_recent(imap_server, user, password)
    url = get_table_url(recent)
    print("✓ Table URL extracted:")
    print(f"  {url}")

    # Validate URL format
    if url.startswith("http"):
        print("✓ URL format looks valid")
    else:
        print("⚠ URL format may be incorrect")
except Exception as e:
    print(f"✗ URL parsing failed: {e}")
    print("\nEmail text sample:")
    recent = fetch_most_recent(imap_server, user, password)
    print(recent.text[:500])
```

**Success Criteria**:
- [ ] URL successfully extracted
- [ ] URL format is valid (starts with http)
- [ ] URL matches expected WRGPT format

**Troubleshooting**:
- If regex fails, examine actual email text
- Update regex pattern in `mail_functions.py:42` if email format changed

---

### Test 1.5: Parse Hole Cards
**Objective**: Verify `fetch_hand()` extracts hole cards from reminder emails

**Test Steps**:
1. Search for reminder/cards email
2. Extract hole cards
3. Verify format

**Test Script** (create `test_hand_parse.py`):
```python
from mail_functions import fetch_hand
import os
from dotenv import load_dotenv

load_dotenv()
imap_server = os.getenv("imap_server")
user = os.getenv("user")
password = os.getenv("password")

try:
    hand = fetch_hand(imap_server, user, password)
    print("✓ Hole cards extracted:")
    print(f"  {hand}")
except Exception as e:
    print(f"✗ Hand parsing failed: {e}")
    print("\nSearching for card emails manually...")
    from mail_functions import Account
    with Account(imap_server, user, password).login() as mb:
        mb.folder.set("INBOX.Poker")
        for msg in mb.fetch():
            if "reminder" in msg.subject.lower() or "cards" in msg.subject.lower():
                print(f"\nFound: {msg.subject}")
                print(f"Date: {msg.date_str}")
                print(f"Sample text:\n{msg.text[:300]}")
                break
```

**Success Criteria**:
- [ ] Function finds card reminder email
- [ ] Extracts hole cards correctly
- [ ] Format matches expected pattern (e.g., "Ah Kd")

**Troubleshooting**:
- If regex fails, check email text format
- Update regex patterns in `mail_functions.py:62-64` if needed
- Verify subject line patterns match actual emails

---

### Phase 1 Summary Checklist
- [ ] Test 1.1: Email Authentication - PASSED
- [ ] Test 1.2: Email Folder Access - PASSED
- [ ] Test 1.3: Fetch Most Recent Email - PASSED
- [ ] Test 1.4: Parse Table URL - PASSED
- [ ] Test 1.5: Parse Hole Cards - PASSED

**Phase 1 Complete When**: All parsing tests pass with archived emails

---

## PHASE 2: Live Tournament Testing
**Can only be tested DURING active tournament**

### Test 2.1: Display Current Hand
**Objective**: Verify `python wrgpt-bot.py hand` displays hole cards

**Test Steps**:
1. Wait for dealer to send hole cards
2. Run: `python wrgpt-bot.py hand`
3. Verify correct cards displayed

**Success Criteria**:
- [ ] Command executes without error
- [ ] Displays current hole cards
- [ ] Cards match what's in email
- [ ] Log entry created

**Expected Output**:
```
! Your hole cards are Ah Kd
```

---

### Test 2.2: Display Table Status
**Objective**: Verify `python wrgpt-bot.py status` displays table in terminal

**Test Steps**:
1. Receive dealer email with table URL
2. Run: `python wrgpt-bot.py status`
3. Verify table status displays in w3m

**Success Criteria**:
- [ ] Command executes without error
- [ ] w3m browser opens
- [ ] Table status displays correctly
- [ ] Shows current players, stacks, pot, action
- [ ] Log entry created

**Troubleshooting**:
- Ensure w3m is installed: `sudo apt-get install w3m`
- Verify URL extraction worked (Phase 1 Test 1.4)
- Test w3m manually with extracted URL

---

### Test 2.3: Send FOLD Command
**Objective**: Verify bot can send fold action to dealer (safest test)

**Test Steps**:
1. Wait for action to be on you
2. Run: `python wrgpt-bot.py fold`
3. Verify email sent to dealer
4. Verify dealer processes fold

**Success Criteria**:
- [ ] Command executes without error
- [ ] Email sent to dealer (check sent folder)
- [ ] Subject line contains player ID
- [ ] Body contains "FOLD"
- [ ] Dealer confirms action
- [ ] Log entry created

**Email Format Expected**:
```
Subject: id=<your_player_id>
Body: FOLD
```

---

### Test 2.4: Send CALL Command
**Objective**: Verify bot can send call action

**Test Steps**:
1. Wait for action to be on you (small bet scenario)
2. Run: `python wrgpt-bot.py call`
3. Verify email sent and processed

**Success Criteria**:
- [ ] Command executes without error
- [ ] Email sent with "CALL"
- [ ] Dealer processes call correctly
- [ ] Log entry created

---

### Test 2.5: Send CHECK Command
**Objective**: Verify bot can send check action

**Test Steps**:
1. Wait for free action (BB pre-flop or no bet)
2. Run: `python wrgpt-bot.py check`
3. Verify email sent and processed

**Success Criteria**:
- [ ] Command executes without error
- [ ] Email sent with "CHECK"
- [ ] Dealer processes check correctly
- [ ] Log entry created

---

### Test 2.6: Send BET Command with Amount
**Objective**: Verify bot can send bet with specific amount

**Test Steps**:
1. Wait for action with betting opportunity
2. Run: `python wrgpt-bot.py bet 100`
3. Verify email sent with correct amount

**Success Criteria**:
- [ ] Command executes without error
- [ ] Email sent with "BET $100"
- [ ] Dealer processes bet correctly
- [ ] Amount matches what you specified
- [ ] Log entry created

---

### Test 2.7: Send RAISE Command with Amount
**Objective**: Verify bot can send raise with specific amount

**Test Steps**:
1. Wait for action with raise opportunity
2. Run: `python wrgpt-bot.py raise 200`
3. Verify email sent with correct amount

**Success Criteria**:
- [ ] Command executes without error
- [ ] Email sent with "RAISE $200"
- [ ] Dealer processes raise correctly
- [ ] Amount matches what you specified
- [ ] Log entry created

---

### Test 2.8: Money Play "Any Amount" Confirmation
**Objective**: Verify safety check when amount not specified

**Test Steps**:
1. Run: `python wrgpt-bot.py call` (without amount)
2. Verify prompted for confirmation
3. Test both yes and no responses

**Success Criteria**:
- [ ] Prompts: "Do you mean to call any amount?"
- [ ] Accepting sends "CALL *"
- [ ] Declining aborts with message
- [ ] No email sent on decline
- [ ] Log entries appropriate

---

### Test 2.9: End-to-End Workflow
**Objective**: Verify complete workflow from email to action

**Test Steps**:
1. Receive dealer email
2. Run `python wrgpt-bot.py status` - view table
3. Run `python wrgpt-bot.py hand` - view cards
4. Make decision
5. Run action command
6. Verify dealer confirms

**Success Criteria**:
- [ ] All commands work in sequence
- [ ] Information is current and accurate
- [ ] Action is processed correctly
- [ ] Workflow feels smooth and usable

---

### Test 2.10: Logging Verification
**Objective**: Verify all actions are logged properly

**Test Steps**:
1. Perform various actions
2. Review log file (check logfile_dir/.wrgpt.log)
3. Verify completeness

**Success Criteria**:
- [ ] Log file created in correct location
- [ ] All actions logged with timestamps
- [ ] Log levels appropriate (INFO, DEBUG)
- [ ] Errors logged if any occur
- [ ] Log format is readable

---

### Phase 2 Summary Checklist
- [ ] Test 2.1: Display Current Hand - PASSED
- [ ] Test 2.2: Display Table Status - PASSED
- [ ] Test 2.3: Send FOLD - PASSED
- [ ] Test 2.4: Send CALL - PASSED
- [ ] Test 2.5: Send CHECK - PASSED
- [ ] Test 2.6: Send BET with Amount - PASSED
- [ ] Test 2.7: Send RAISE with Amount - PASSED
- [ ] Test 2.8: "Any Amount" Confirmation - PASSED
- [ ] Test 2.9: End-to-End Workflow - PASSED
- [ ] Test 2.10: Logging Verification - PASSED

**Phase 2 Complete When**: All live tournament tests pass

---

## Known Issues to Monitor

From code TODOs and potential problems:

1. **Case Sensitivity** (wrgpt-bot.py:28)
   - Yes/no prompts are case-sensitive
   - Works but could be cleaner

2. **Exception Handling** (wrgpt-bot.py:78)
   - Non-integer amounts not gracefully handled
   - Monitor for crashes with bad input

3. **Missing Confirmation** (wrgpt-bot.py:121)
   - No stdout summary after sending
   - User doesn't get confirmation message

4. **Email Provider Differences**
   - Folder names may differ
   - Email formats may have changed
   - Regex patterns may need updates

---

## Validation Criteria

### Base Model is VALIDATED when:
- ✅ All Phase 1 tests pass
- ✅ All Phase 2 tests pass
- ✅ At least one full tournament hand played successfully
- ✅ Known issues documented (but not necessarily fixed)
- ✅ `.env` template/example created

### Only After Validation:
- Move to Enhanced Model phase
- Create `PLAN-ENHANCED.md`
- Begin web UI development

---

## Testing Notes

### Pre-Tournament Setup
1. Create all test scripts from Phase 1
2. Run Phase 1 tests with archived emails
3. Fix any issues found
4. Document email formats for reference
5. Create `.env.example` template

### During Tournament
1. Run Phase 2 tests opportunistically
2. Don't risk critical hands with untested features
3. Fall back to manual email if bot fails
4. Document any unexpected behaviors
5. Complete testing over multiple hands/sessions

### Post-Tournament
1. Review all logs
2. Document lessons learned
3. Update this test plan with findings
4. Create issues list for known problems
5. Decide: fix issues or move to Enhanced Model?
