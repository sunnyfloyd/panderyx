# Panderyx

Web application that provides a user-friendly codeless interface for data manipulation and analysis.0,

## Application Design

- One-page application with the user interface being managed by React
- Creation/clicking on the block/node will trigger API like request to Django view that will return a rendered HTML response (block config or workflow output) that will be handled using AJAX so that the page does not reload after submitting a form/running a workflow
- User can use an application only after registration and login
- React/Svelte user interface
- Each project is representeded as project class instance; each project is built from blocks that represent different steps in project flow. Project on its own does not store any data - it only stores a reference to a data that is fed into the project.
- Each building block should be based on a class and or a class method
- Each block should have a configuration fields that can be populated by a user
- Each block should provide the preview of its input and output
- Conditions and loops should be simplified compared to Alteryx

## Planned Features

### Minimum

- input/output block
- joining block
- union block
- unique/duplicate block
- groupby block
- pivot block
- filter block
- date-time parsing block
- sample block
- sort block
- transpose

### Fully Featured

- formula block (?)
- browse block
- chart block
- loop with loop count
- workflow condition (not filter related)
- variable block
