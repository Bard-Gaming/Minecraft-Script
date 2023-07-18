# Minecraft Script
### To do:
- [ ] Make build function to parse to mcfunction
- [ ] make args better
	- [ ] build \[>\] \[filename\]:
		- "build" : prints output
		- "build >": outputs to out.mcfunction
		- "build > filename" outputs to filename.mcfunction (auto adds .mcfunction if no extension)
		
	- [ ] run \*\[filename\]
		- "run" : locates .mcs files and asks to run (prints to console)
		- "run \*filename" : runs files added

### Ideas:
- log() to log (print) values with interpreter
- player for player actions
- cmd() for commands that aren't supported yet (I suppose, gotta start somewhere)