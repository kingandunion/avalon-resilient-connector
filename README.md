# Avalon for IBM Resilient

This package contains components that manage Avalon workspaces from IBM Resilient. 

User needs to obtain API token from [Avalon](https://avalon.kingandunion.com).

## Installation

Prerequisites:

```
resilient-circuits >=v30.0.0
```

To install in "development mode":

```
pip install -e ./avalon/
```

After installation, the package will be loaded by `resilient-circuits run`.

To uninstall:

```
pip uninstall avalon
```

To package for distribution:

```
python ./avalon/setup.py sdist
```

The resulting .tar.gz file can be installed using:

```
pip install fn_avalon<version>.tar.gz
```

## Configuration

1. Import the package's customization data into the Resilient Platform through the command:

	```
	resilient-circuits customize
	```
	
	This will create the following custom components:        
	
	* Message Destinations: `avalon.create_workspace`

2. Update and edit `app.config` by first running:

	```
	resilient-circuits config [-u | -c]. 
	```
		
	Then edit the `[avalon]` section:
	
	```
	[avalon]
	base_url=<avalon-base-url>
	api_token=<avalon-api-token>
	```

