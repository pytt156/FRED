# Way of Working

## Branching
- `main` is the stable branch.
- All work is done in feature branches.
- Branch naming examples:
  - `edge/display`
  - `backend/state-engine`
  - `simulation/room-data`

## Pull Requests
- Changes are merged into `main` through pull requests.
- PRs should briefly describe:
  - what changed
  - why
  - how it was tested
- PRs should be small enough to review easily.

## Issues
- Development tasks are tracked as GitHub Issues.
- Each issue should describe one concrete piece of work.
- Relevant PRs should link to the issue they resolve.

## Kanban
Tasks are tracked in GitHub Projects.

Columns/statuses:

- Backlog
- Ready
- In Progress
- Review
- Done

Only tasks that are clear enough to start should move to `Ready`.

## Definition of Done
A task is Done when:
- the implementation is complete
- relevant testing has been performed
- documentation is updated if needed
- the change is merged into `main`

## Communication
- Discord is used for discussion and quick decisions.
- GitHub is the source of truth for code, tasks and technical documentation.
- Important project decisions should be reflected in the repository documentation.

## Working split
The project is broadly split into:

**Edge / Device**
- hardware
- sensors
- MicroPython
- networking
- MQTT
- display

**Backend / Pet Brain**
- MQTT backend
- room state
- pet state
- PostgreSQL
- Grafana

Shared interfaces such as MQTT topics and payload formats are decided together.