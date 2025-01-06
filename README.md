# cliconf

> [!NOTE]
> This project is still work in progress, usage may change in near future. 

Python library for creating persistent CLI configuration files, currently it supports being able to 
create configuration files in `yaml` or `json`. Going forward will continue to extend if I see a different file type 
that serves as a nice way to store persistent config for a CLI in the same ways that `json` and `yaml` can.

## Usage 
For the purposes of the example lets say that we have an example CLI application using [typer](https://typer.tiangolo.com/)
and, you want to write a command that inits a config file based on a variable that a user provided. 

Below is some example usage for if you wanted to write a config file in `yaml`: 

```python
import typer as t 
from typing import Annotated

from cliconf.configurer import Configurer

app: t.Typer = t.Typer()

@app.command(
    help="Will create a new yaml configuration file, storing whatever is provided by you :)",
    short_help="creates a new yaml configuration file",
)
def init(config_object: Annotated[dict[str], t.Argument()]): 
    configurer: Configurer = Configurer(file_type="yaml", config=config_object, path=None, app_name="ExampleApp")
    configurer.safe_initialize()
```

In the above example, we use `safe_initialize` as we want to make sure that the file doesn't already exist before we create it. 
