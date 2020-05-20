# Why?

Sometimes I run long scripts on a remote machine and I want to know when they finish. It's
not urgent enough that I need a text or toot, but being able to pull up a simple page that
shows what is done and not done makes it easy to check periodically.

# How?

This tiny Flask API runs on a server (Raspberry Pi, etc.). It has very basic authentication
and waits for a curl (or similar) GET request with some small amount of data. The data are
displayed on a simple web page.

The reason for a simple GET request is to make this as code-agnostic as possible. Drop a 
curl command into R or Python or Go or Ruby or whatever (I assume) and be able to watch 
whatever data you pass.

You can either run with the internal Flask development server or something like gunicorn.

# Other Use Cases?

I'm sure there are some.

# Security?

I'm sure this isn't very secure. It has basic data cleaning, string length limits, and
username/password protection. There is no database--all data are kept in memory and will 
disappear when the server is stopped. Use at your own risk, don't reuse passwords, and 
obviously don't pass data that can't be shared openly online. The last part includes things
like "front_door_unlocked"--use common sense.