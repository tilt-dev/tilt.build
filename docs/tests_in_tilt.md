---
title: Tests in Tilt
description: "Run your tests from Tilt for visibility, responsiveness, and fine-grained control."
layout: docs
---
With the Tilt `test` primitive, you can run your tests from Tilt itself. Take advantage of Tilt's file-watching and responsiveness, and the power and customizability of Starlark, to supercharge your testing workflow.

## How to Use It
Define tests in your Tiltfile with the `test` primitive:
```python
# TODO: examples
```

Your tests will appear in their own section of the overview grid, and alerts will be reflected on the test cards and in the status bar, so that you know at a glance when something is wrong.

[screenshot of overview with tests (including red test(s)]

Just like any other workload managed by Tilt, you can drill into a test and see logs and other details.

In the log view, you can filter the sidebar by item type: Resources (generally, the app you're developing and associated workflows: your Kubernetes workloads, local resources, etc.), Tests, or both. You can also toggle "Alerts On Top" sorting, to make it even more visible when something has gone wrong and needs your attention

[screenshot of sidebar including "alerts on top" sorting]

### When Tests Run
In a syntax you may recognize from `local_resource`, you can associate files with a test via the `deps=[...]` parameter. When any of these file dependencies change, Tilt will re-execute the test:

```python
# A test depending on an entire directory
test('cart-tests', 'go test ./pkg/cart', deps=['./pkg/cart'])

# A test depending on specific relevant files
test('unit-test-remittance', 'pytest remittance_test.py',
     deps=['app/remittance.py', 'app/remittance_test.py', 'app/payment_utils.py'])
```
(More on how to intelligently set your dependencies below.)

Sometimes, you don't want your test(s) to execute automatically. Maybe you want to turn off automatic-ness for all but a few tests you're iterating on, or prevent an expensive integration test from running all the time. Use the "auto" trigger in the UI to toggle automatic execution on or off for a given test.

[screenshot of auto toggle(s)]

You can also set default AUTO values for your tests via the Tiltfile, using [the `trigger_mode` parameter](https://docs.tilt.dev/manual_update_control.html).

### Programmatically Registering Tests
Part of what's great about Starlark (the dialect of Python that Tiltfiles are written in) is that it's a _programming language_, so you can use it for complex stuff. In particular, you can use it to programmatically register your tests to Tilt in whichever way works best for you. Here are some examples:

#### Go tests by package
This approach assumes that your unit tests run pretty quickly, so it's not too expensive to test an entire package when code is changed.

Note that you can pass any flags you want to your `go test` call--you can, for instance, combine this with specific build conditions (see, for example, [this slow test file](https://github.com/tilt-dev/tilt/blob/ba1de77456a46ff72f5de798aaac092f47f481e7/internal/build/container_test.go#L1); invoking `go test -tags skipcontainertests` will skip this file).
```python
def all_go_package_dirs():
  pkgs_raw = str(local('go list -f "{{.Dir}}" ./...')).rstrip().split("\n")
  pkgs = []
  for pkg in pkgs_raw:
    cleaned = pkg.strip()
    if cleaned:
      pkgs.append(cleaned)

  return pkgs

for pkg in all_go_package_dirs():
  name = os.path.basename(pkg)  ## TODO: this is broken ugh
  test(name, 'go test %s' % pkg, deps=[pkg])
```


#### JS tests by test file
This snippet naively matches by prefix--e.g. `foo_test.tsx` will run on changes to `foo.tsx` and `foo_test.tsx`. Note that it's written for a flat file hierarchy (i.e. all the JS files and tests live at the root of `web/src`, but is easy to modify to fit your directory structure).
```python
web_src_files = [os.path.basename(f) for f in listdir('web/src')]
test_files = [f for f in web_src_files
              if f.endswith('test.tsx')]

for tf in test_files:
  cmd = "cd web && yarn test --watchAll=false %s" % tf
  slug = tf.replace('.test.tsx', '')
  deps = [os.path.join('web/src/', f)
          for f in web_src_files
          if f.startswith(slug)]
  test(slug, cmd, deps=deps)
```

### And more?!
We hope to offer more snippets soon, for more languages, test frameworks, and directory structures. Got an interesting use case that you'd like help configuring? Let us know!

## Future Work
* ability to tag tests, and use those tags to sort/filter/run tests
* timeouts for test
* make it easy to run tests against the services in your cluster that Tilt is already managing
* better language-specific logic for registering all your tests
