(() => {
    const select = document.querySelector('.js-custom-select');
    const choices = new Choices(select, {
        searchEnabled: false,
        itemSelectText: '',
        classNames: {
            containerOuter: 'defselect',
            containerInner: 'defselect__inner',
            input: 'defselect__input',
            inputCloned: 'defselect__input--cloned',
            list: 'defselect__list',
            listItems: 'defselect__list--multiple',
            listSingle: 'defselect__list--single',
            listDropdown: 'defselect__list--dropdown',
            item: 'defselect__item',
            itemSelectable: 'defselect__item--selectable',
            itemDisabled: 'defselect__item--disabled',
            itemChoice: 'defselect__item--choice',
            placeholder: 'defselect__placeholder',
            group: 'defselect__group',
            groupHeading: 'defselect__heading',
            button: 'defselect__button',
            activeState: 'is-active',
            focusState: 'is-focused',
            openState: 'is-open',
            disabledState: 'is-disabled',
            highlightedState: 'is-highlighted',
            selectedState: 'is-selected',
            flippedState: 'is-flipped',
            loadingState: 'is-loading',
            noResults: 'has-no-results',
            noChoices: 'has-no-defselect'
          }
    });
}

)();