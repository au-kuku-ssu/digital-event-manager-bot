# 📋 Reports Evaluation Bot

This bot handles the **authorization and evaluation process** for reports (e.g., at scientific events or academic defenses).

It handles:
- Authorization (`JURY-1`, `JURY-2`, `CHAIR`)
- Report scoring & commenting
- Viewing results
- Editing scores (for chair)
- Full support for state cleanup & localized strings (currently lang is hardcoded)

---

## 🎯 Tasks

A list of known issues, tech debt, and upcoming improvements:

- **Implement a real database.**
  Right now we're working with placeholders. Need to switch to a real database and bind data logic to it.

- **Insecure presentation scoring implementation.**
  Currently, the editing of scores is done through passing the `jury_code` in the callback data, which is not secure. Hashed version must be used.
  It would be better to avoid passing sensitive information like this directly and instead use a more secure method of handling such data, like using a database or encrypted session tokens.

- **Write proper tests.**
  Everything needs testing — especially evaluation logic, state transitions, and error cases.

- **Add proper logging.**
  Right now, debugging is a pain. We need proper `logging` for errors, state transitions, and user actions.

- **Prevent access to regular evaluation during edit.**
  We should check whether the user is currently editing reports, and if so, block standard evaluation flow to avoid data collisions.

- **Implement dynamic language selection.**
  `lang="ru"` is currently hardcoded. Need a persistent, user-defined language choice with fallback to `ru`.

- **Refactor repeated logic.**
  Shared patterns like message deletion, state clearing, and button generation should be abstracted. Move UI code from `handlers.py` into corresponding `keyboards.py`.

- **Add race condition checks.**
  Especially around score submission and editing — ensure two parallel actions don’t conflict or overwrite each other.

- **Move more logic into `services/`.**
  Separate frontend concerns (keyboards, responses) from business logic. Need to avoid bloating corresponding `handlers.py`.

- **More problems exist.**
  I forgor💀. Check back later or audit the code for more issues ✨

---

## 🚪 Authentication

Users must first **authorize** themselves to access any evaluation features.

### ✅ Current Accepted codes:

| Code     | Role   |
|----------|--------|
| JURY-1   | Jury   |
| JURY-2   | Jury   |
| CHAIR    | Chair  |

### 🔄 Flow:
- Start: `cb_re_main` → `frontend_cb_re_auth`
- User is prompted to enter a code
- Handled in: `st_re_process_code`
- After **3 invalid attempts**, user is sent back to the main menu.

---

## 🧭 Main Menu Navigation

### Triggered:
- After successful auth
- Or manually via: `cb_re_main_menu`

### Return to Main Menu:
- User taps “Return to Main Menu” → handled via `cb_re_return_to_main_menu`
- State is **cleared**

---

## 🧑‍⚖️ Report Evaluation Flow

| Step                | Trigger                                   | Handler Function                          |
|---------------------|-------------------------------------------|--------------------------------------------|
| View presentations  | `cb_re_pres_page:{pres_page}`             | `frontend_cb_re_show_presentations`        |
| Select report       | `cb_re_choose_pres:{pres_id}`             | `frontend_cb_re_eval_choose_presentation`  |
| Score report        | `cb_re_score:{criterion}:{score}`   | `frontend_cb_re_eval_handle_score`         |
| Go back in scoring  | `cb_re_return_to_score:{criterion}` | `frontend_cb_re_eval_return_to_score`      |
| Add comment         | `cb_re_eval_comment`                      | `frontend_cb_re_eval_comment`              |
| Comment message     | (message input)                           | `st_re_eval_comment`                       |
| Confirm submission  | `cb_re_eval_marks_accepted`               | `frontend_cb_re_eval_marks_accepted`    |

---

## 📊 Results Table

- View scores: `cb_re_results_page:` → `frontend_cb_re_results_table`
- If no presents available, displays message

---

## ✏️ Edit Results (Chair Only)

- Start edit flow: `cb_re_edit_results`
- Choose jury: `cb_re_edit_select_jury:{jury_id}`
- Select presentation: `cb_re_edit_pres_page:{pres_page}`
- Then handled like report evaluation

---

## 📁 Project Structure Overview
```
.
├── fsm_states.py # All FSM states declared here
├── router.py # Bot route declarations
├── utils.py # General-purpose helper functions
├── locale/ # Language files (en.yml, ru.yml)
├── data/ # Dummy or static data (jury, presentations)
│
├── features/
│ ├── auth/ # Authorization logic
│ ├── evaluation/ # Core evaluation flow
│ │ └── edit_reports/ # Nested edit menu for CHAIR
│ ├── main_menu/ # Main menu display logic
│ └── results_table/ # Display results table
│       └── [handlers.py, keyboards.py]  # All subfolders follow this structure
├── services/
│ └── evaluation.py # Business logic (non-bot-specific)
```
