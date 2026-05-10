# Commands

- add
- update
- delete
- mark-in-progress
- mark-done
- list
- list by status

Task schema:

- id
- description
- status
- createdAt
- updatedAt

Core functions:

- load_tasks
- save_tasks
- get_next_id
- find_task
- add_task
- update_task
- delete_task
- mark_task
- list_tasks

Edge cases:

- missing file
- bad JSON
- invalid ID
- invalid status
- empty description
