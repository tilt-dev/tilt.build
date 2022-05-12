---
title: Sharing Snapshots
description: "Share Tilt state with snapshots for remote or async debugging"
layout: docs
sidebar: guides
---

Snapshots save your Tilt state to a file, so you (or another Tilt user) can later load that file, and interactively explore logs and error status for that moment in time. This can help with async debugging, and add context to bug reports. 

Snapshots were once part of the since-deprecated Tilt Cloud, but are now offline-only.

## Via Command Line

With a Tilt session running, run `tilt snapshot create <file>` to create a JSON file.

Then, run `tilt snapshot view <file>` to view the Snapshot.

A header on the top of the screen shows that you're viewing a Snapshot.

<figure>
  <img src="/assets/docimg/snapshots-header.png" style="width:500px; height: auto;" title="Snapshots Header">
</figure>


## Via Tilt Web

Create a Snapshot by clicking <img src="/assets/docimg/snapshots-icon.png" title="Snapshots Icon" style="width:35px; height: auto; margin-left: 5px; margin-right: 5px;">on the top-right of the screen, then clicking the "Save Snapshot" button.

To view the downloaded Snapshot, run `tilt snapshot view <file>` in your Terminal.

<figure>
  <img src="/assets/docimg/snapshots-menu.png" style="width:500px; height: auto;" title="Snapshots Menu">
</figure>
