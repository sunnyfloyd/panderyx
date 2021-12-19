# Panderyx

Web application that provides a user-friendly codeless interface for data manipulation and analysis.

## Application Design

- One-page application with the user interface developed in Vue.js.
- Creation/clicking on the block/node will trigger a request to Django view route that will return a rendered HTML response (block config or workflow output) that will be displayed using Vue in a seperate view/div/web page section. Response will be then handled using AJAX so that the page does not reload after submitting a form/running a workflow, but instead GET/POST/PUT request is made using Vue
- Views will be accessed by a dynamic endpoints like `<workflow_id>/<block_id>`; if block_id will be already existing in a database for this workflow the rendered form will be prepopulated with data from a DB. Otherwise it will return an empty form
- Parent of an element will be added on the client's end via Vue as a hidden form input. Child(ren) should be populated on the server side (TBD whether children are required to be passed to the client)
- User can use an application only after registration and login
- Vue user interface
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

## TO-DO

- Create new Config class that will store config fields and config methods; each tool would use different config class that inherits from main Config class.
- Config class would be a dataclass or a class validated with the use of pydantic.
- Each config field would be defined by a different class (int, str, custom class) that would validate whether passed value is correct. It would also allow for indication whether given field is required or not by passing some `is_required` parameter.
