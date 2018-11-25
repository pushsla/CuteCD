# Cute CD
**versions of GNU cd written on Golang and Python**
## Idea
I want to do something more than standard **cd**, but solve similar problems. Sometimes, working in a terminal, it's very annoying to prescribe long paths to folders, especially if you do not remember them exactly. Recursive search can save time. I do NOT replace the **cd**, but try to provide an instrument that saves my time and nerves.

## What is already done
At the moment, single-threaded recursive search is implemented, and you can
* select the start point of search
* search for a full name match, or by a pattern (in GO pattern must match the end of name)
* choice of several suitable folders (only in GO version)
* case-insensitive/case-sensitive matching modes
* chose one from multiplie found folders, or chdir to first found
* search all directories, or exclude hidden (only in Python version)
* set search depth limit

## Known bugs
* Zsh drops out with segfault if use GO version

## How to use
### Python version
**Synopsis**<br>
    ccd [search name or pattern] [keys] (in any order)

**Keys**<br>
    -d <path>	set start search point. Default -- $HOME value<br>
    -f		make chdir to the first found directory, will be no choice<br>
    -p		interpretate [name] as a regular search pattern. Default -- [name] must coincide with dir name.<br>
    -l 		case unsensitive search. Default -- case sensitive<br>
    -a		search in hidden directories. Default -- dont search in hidden<br>
    -r <value>	set search depth limit. Do not set big values. Default -- 100<br>
    -c <path>	try use specefied config file

**Config file**<br>
CuteCD also uses configuration file. It will be created at first use as $HOME/.config/ccd.conf
Config options:
* ***[Default]*** -- section with parameters that can be overwritten by flags use
  * start_point -- default root of searching (flag -d/second request)
  * search_by_pattern -- interprete request string as regular pattern, not as dir name (flag -p)
  * include_hidden_files -- search in/for hidden dirs (flag -a)
  * search_til_first -- make chdir to the first found directory (flag -f)
  * max_depth -- maximum search depth (flag -r)
  * case_sensitive -- case sensitive search (flag -l)
* ***[Rules]*** -- rules of search for adjusting search performance and decrease search time and result list
  * excluded_dirs -- dont search in these dirs. Syntax fullpath1:fullpath2...
  * exclude_pattern -- dont search in dirs with names matching pattern. Standart Python re syntax.

### GO version (Outdated functionality)
**Synopsis**<br>
    ccd [DIR_NAME] [START_DIR] [KEYS]<br>
  in any order<br>

**Keys**<br>
-p 		match dirs by name pattern, not by name<br>
-c    	for case-sensitive matching. By default search is NOT case-sensitive<br>
-y    	will abort program and make cd to FIRST found directory<br>
-n    	will find all matched dirs (by default)<br>
-r    	you can set recursion limit. Please, dont set values greater then 1000. Default - 100<br>
-s    	you can set start directory. By default - your $HOME directory<br>
          		(WILL BE DEPRECATED SOON BECAUSE OF USELESS)<br>
          		(YOU MAY NOT USE THE KEY TO SET START DIR. JUST SET IT AFTER [DIR_NAME] IN THE SAME WAY)<br>
-d    	output debug message contains search parameters<br>

**Examples**<br>
* ccd Documents<br>
  * will find dirs with names matching 'Documents' in your $HOME and give you choice where to cd<br>
* ccd uments -p<br>
  * will find dirs with names, matching pattern '^.*uments$' in your $HOME and give you choise where to cd<br>
* ccd uments -p -y<br>
  * will find dirs with names, matching pattern '^.*uments$' in your $HOME and make cd to first found dir.<br>
* ccd share -s /<br>
  * will find dirs with names matching 'share' in / directory and give you choice where to cd<br>
* ccd share -p /<br>
  * will find dirs with names matching '^.*share$' in / directory and give you choice where to cd<br>

**Short demo**<br>
<img src='https://i.imgur.com/TLr4Gzo.gif'/>
