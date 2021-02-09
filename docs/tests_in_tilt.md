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
- part of what's great about starlark is that it's a programming language, so you can do complicated stuff
- here's an example of registering your js tests by prefix:

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

- here's an example of registering your go tests by directory
- we hope to offer more snippets/fast setup instructions per language soon

## Future Work
- tags
- timeout
- easy to run tests against your cluster
- better language-specific logic for registering all your tests
