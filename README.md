# hydrus-url-hole
Preprocess urls when you have too many tabs, and they aren't in the correct form for hydrus.

##How to define a rule
Add an item to the filters array
If an action you want is already defined it might be as easy as calling it with you match
An entry takes the form

`(url_pattern,function,parameters)`

So for example

```python
def add_subscription(u,param,match):
    name=unquote(match.group(1))
    put_subscription(param,name)
    return None #Returning none will cause this rule to terminate, to indicate failure return False

filters=(
 #Items aove this rule take precedence over it
 (r"https{0,1}://twitter.com/([^/]+)/{0,1}",add_subscription,"twitter.com")
 )
```

### Actions
An action takes some programatically defined action, it will always be passed
`(u,param,match)`

**Parameters**
- `u`: The url
- `param`:Any object you pass from the filters list
- `match`: The result of re.match

**Return values**
- `string`: A string to continue evaluating rules with
- `None`: Stop evaluating rules
- `False`: Indicate that evaluating the rule failed
