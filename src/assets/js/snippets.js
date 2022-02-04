(function() {
  const tagInitializer = () => {
    if (document.readyState !== 'complete') {
      return
    }

    const tagIds = {}
    const allSnippets = document.querySelectorAll('.Docs-snippets-item')
    allSnippets.forEach(el => {
      el.getAttribute('data-tags').split(' ').forEach((tag) => {
        var ids = tagIds[tag]
        if (ids === undefined) {
          ids = tagIds[tag] = []
        }
        ids.push(el.id)
      })
    })

    const buttonsEl = document.querySelector('.Docs-snippets-tag-cloud')
    const tagButtons = []
    Object.keys(tagIds).sort().forEach((tag, i) => {
      const button = document.createElement('button')
      button.setAttribute('type', 'button')
      button.classList.add('Docs-snippet-tag-button')
      setButtonSelected(button, false)
      button.innerHTML = tag
      button.onclick = button.onKeyDown = (e) => {
        const tag = e.target.innerHTML
        const selected = setButtonSelected(e.target, !e.target.getAttribute('data-selected'))
        const tags = searchTags()
        if (selected) {
          if (tags.indexOf(tag) === -1) tags.push(tag)
        } else {
          if (tags.indexOf(tag) >= 0) tags.splice(tags.indexOf(tag), 1)
        }
        history.pushState('', document.title, window.location.pathname + '?' + encodeURIComponent(tags.join(' ')))
        updateVisibleSnippets()
      }
      buttonsEl.append(button)
      tagButtons.push(button)
    })

    const clear = document.createElement('a')
    clear.innerHTML = "clear"
    clear.hidden = true
    clear.onclick = clear.onKeyDown = (e) => {
      tagButtons.forEach(b => {
        setButtonSelected(b, false)
      })
      history.pushState('', document.title, window.location.pathname)
      updateVisibleSnippets()
    }
    buttonsEl.append(clear)

    function setButtonSelected(button, selected) {
      button.setAttribute('data-selected', selected ? 'true' : '')
      if (selected) {
        button.classList.add('tag-selected')
      } else {
        button.classList.remove('tag-selected')
      }
      return selected
    }

    function updateVisibleSnippets() {
      const selectedTags = tagButtons.
            filter(tb => tb.getAttribute('data-selected')).
            map(tb => tb.innerHTML)

      clear.hidden = selectedTags.length === 0

      console.log("updateVisibleSnippets: " + selectedTags.join(" "))
      allSnippets.forEach(el => {
        if (selectedTags.length === 0) {
          el.hidden = false
        } else {
          if (el.getAttribute('data-tags').split(' ').filter(t => selectedTags.indexOf(t) !== -1).length > 0) {
            el.hidden = false
          } else {
            el.hidden = true
          }
        }
      })
    }

    function searchTags() {
      if (!window.location.search) return []
      return decodeURIComponent(window.location.search.slice(1)).split(' ')
    }

    function setSelectedTags() {
      const selectedTags = searchTags()
      tagButtons.forEach(b => {
        setButtonSelected(b, selectedTags.indexOf(b.innerHTML) >= 0)
      })
    }
    function refreshState() {
      setSelectedTags()
      updateVisibleSnippets()
    }
    // set up button state on initial page load
    refreshState()
    window.onpopstate = () => { console.log("popstate"); refreshState() }
  }

  document.addEventListener('readystatechange', tagInitializer)
})()
