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

- create tests for len properties for both Workflow and Tool classes (Tool methods should be tested in a new test class)
- tool errors should be added to `self._errors` on tool and exposed when tool is created/modified
- `workflow_exceptions.ToolNotAvailable` should be handled in the view
- Those fragments should also handled by internal Workflow `add_tool_input` method

```py
# ...
if input_ids is not None:
    input_ids = self._clean_tool_ids(input_ids)
    for input_id in input_ids:
        tool.add_input(input_id)

if output_ids is not None:
    output_ids = self._clean_tool_ids(output_ids)
    for output_id in output_ids:
        tool.add_output(output_id)
# ...
```
- Same as above should be applied for `remove_tool` using `remove_tool_input` method
- Separate method for initializing config (maybe config fields in the future)
