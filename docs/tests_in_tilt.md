---
title: Tests in Tilt
description: "Run your tests from Tilt for visibility, responsiveness, and fine-grained control."
layout: docs
---
With the Tilt `test` primitive, you can run your tests from Tilt itself. Take advantage of Tilt's file-watching and responsiveness, and the power and customizability of Starlark, to integrate testing with the rest of your Tilt workflow.

## How to Use It
Define tests in your Tiltfile with the `test` primitive:
```python
test('cart-tests', 'go test ./pkg/cart', deps=['./pkg/cart'])
test('py-tests', 'pytest app/', deps=['app/'])
test('slow-integration-test', 'tests/integration.sh',
     trigger_mode=TRIGGER_MODE_MANUAL, auto_init=False)
```

`test` supports all the same arguments as `local_resource` [see API reference](https://docs.tilt.dev/api.html#api.local_resource). The only notable difference today is that for tests, parallelism is _on_ by default (i.e. the default of `allow_parallel=True`).

Your tests will appear in their own section of the overview grid, and alerts will be reflected on the test cards and in the status bar, so that you know at a glance when something is wrong.

<figure>
    <img src="/assets/img/tests-in-tilt/overview-with-tests.png" alt="the Tilt UI overview page, with several tests">
    <figcaption>Tests appear in their own section of the overview, and test status is summarized in the status bar at the top of the page</figcaption>
</figure>

Just like any other resource managed by Tilt, you can drill into a test and see logs and other details.

In the log view, you can filter the sidebar by item type (if, say, you want to see only tests, or you want to filter tests out and focus on your app in the cluster). You can also toggle "Alerts On Top" sorting, to make it even more visible when something has gone wrong and needs your attention

<figure>
    <img src="/assets/img/tests-in-tilt/sidebar-alerts-on-top.png" alt="sidebar displaying only tests, with alerts sorted to the top">
    <figcaption>Here's an example of sidebar filtering (displaying only tests). In "Alerts on Top" mode, any cards with alerts are sorted to the top of the sidebar for easy visibility</figcaption>
</figure>

### When Tests Run
Just as with a `local_resource`, you can associate files with a test via the `deps=[...]` parameter. When any of these file dependencies change, Tilt will re-execute the test:

```python
# A test depending on an entire directory
test('cart-tests', 'go test ./pkg/cart', deps=['./pkg/cart'])

# A test depending on specific relevant files
test('unit-test-remittance', 'pytest remittance_test.py',
     deps=['app/remittance.py', 'app/remittance_test.py', 'app/payment_utils.py'])
```
(More on how to intelligently set your dependencies below.)

Sometimes, you don't want your test(s) to execute automatically. Maybe you want to iterate on a few tests and disable the rest, or prevent an expensive integration test from running all the time. Use the "auto" slider in the UI to toggle automatic execution on or off for a given test.

<figure>
    <img src="/assets/img/tests-in-tilt/auto-toggles.png" alt="a close-up of several cards in the sidebar, with 'auto/manual' toggles visible">
    <figcaption>The 'auto/manual' toggle (visible on hover) allows you to control whether a given test runs automatically when its deps change.</figcaption>
</figure>

You can also control this behavior via the Tiltfile, using [the `trigger_mode` parameter](https://docs.tilt.dev/manual_update_control.html).

### Programmatically Registering Tests
Part of what's great about Starlark (the dialect of Python that Tiltfiles are written in) is that it's a _programming language_, which makes Tiltfiles extremely flexible. Here are some examples of different ways you can register your tests to Tilt.

#### Your entire unit test suite
If your whole unit test suite runs relatively quickly/has caching (like Go tests), you can just run the whole thing when relevant files change:
```python
def all_go_files(path):
  return str(local('find . -type f -name "*.go"')).split("\n")

test('go-tests', 'go test ./... -timeout 30s', deps=all_go_files())
```

#### Go tests by package
Here, your tests are split into different cards (one per Go package). This approach gives you both more control over when certain tests run (in the snippet below, tests for package `foo` run only when a file in directory `foo` changes), and more visibility into what is going wrong (because tests are broken up more, so it's easier to see what failed).

The trade-off for speed and visibility here is looser matching between files and the tests they affect (the above example will rerun tests for package `foo` when its files _or anything it depends on_ change).
```python
CWD = os.getcwd()

def all_go_package_dirs():
  pkgs_raw = str(local('go list -f "{{.Dir}}" ./...')).rstrip().split("\n")
  pkgs = []
  for pkg in pkgs_raw:
    cleaned = pkg.strip()
    if cleaned:
      pkgs.append(cleaned)

  return pkgs

def pretty_name(s):
  return s.replace(CWD, '').lstrip('/')

for pkg in all_go_package_dirs():
  name = pretty_name(pkg)
  test(name, 'go test %s' % pkg, deps=[pkg])
```

#### JS tests by test file
Alternately, you can split your tests up even further, into one card per test file.

This snippet naively matches by prefix--e.g. `foo.test.tsx` will run on changes to `foo.tsx` and `foo.test.tsx`. Note that it's written for a flat file hierarchy (i.e. all the JS files and tests live at the root of `web/src`), but is easy to modify to fit your directory structure.
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
