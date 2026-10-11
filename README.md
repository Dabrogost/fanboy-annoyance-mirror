# Fanboy's Annoyance List — uBO build mirror

Independent, automatically generated distribution of **Fanboy's Annoyance List (uBlock Origin edition)** for [Chroma Ad-Blocker](https://github.com/Dabrogost/Chroma-Ad-Blocker).

The filtering rules are **not authored or maintained here**. The authoritative upstream is [easylist/easylist](https://github.com/easylist/easylist), using its [`fanboy-annoyance-uBO.template`](https://github.com/easylist/easylist/blob/master/fanboy-annoyance-uBO.template). This mirror simply compiles those upstream files and publishes a single subscription URL. This project is not affiliated with or endorsed by EasyList/Fanboy.

## Subscribe

After the first successful GitHub Actions build, the generated list is served at:

```text
https://raw.githubusercontent.com/Dabrogost/fanboy-annoyance-mirror/main/fanboy-annoyance.txt
```

The file is generated during the first successful run; this URL will return 404 until then.

## Automated updates

GitHub Actions runs twice daily (05:17 and 17:17 UTC) or on demand under **Actions → Build Fanboy Annoyance uBO → Run workflow**.

The workflow:

1. Clones the latest EasyList repository.
2. Installs the same `python-abp` `flrender` compiler used in EasyList's official build workflow.
3. Renders `fanboy-annoyance-uBO.template` as one combined list.
4. Validates the output is plausible and contains uBO scriptlets.
5. Commits and publishes only when the filtering rules change (ignores build-timestamp-only differences).

If the upstream fetch, compilation, or validation fails, the workflow fails **without replacing the previously published list**.

## Chroma integration

Point the default Fanboy subscription at the generated URL in `extension/subscriptions/lists.js`. Retain `cosmeticOnly: true` so Chroma continues to handle cosmetic and scriptlet rules without adding this list's network rules to dynamic DNR rules.

Validate an initial successful update before switching Chroma's default subscription. The counts from the previous cached subscription (45,960 cosmetics and 2,781 scriptlets as of October 10, 2026) are useful reference figures, but will change with upstream edits and Chroma's supported-scriptlet filtering.

## Credits and licensing

All rules and source templates are upstream EasyList/Fanboy work. See [EasyList's licensing information](https://easylist.to/pages/licence.html) and [upstream repository](https://github.com/easylist/easylist). Preserve the generated list's attribution and header when redistributing.
