{
  class Vue {
    constructor({el, data, methods}) {
      this.data = data;
      this.importData(data);
      this.importMethods(methods);
      this.elRoot = document.querySelector(el);
      this.interpolationBraces = ['{{', '}}'];
      this.renderFragments = {
        interpolation: [],
        bind: [],
        if: [],
      };
      this.initFragments();
      this.initBoundEvents();
      this.render();
    }

    importData(data) {
      Object.entries(data).forEach(([key, value]) => {
        const getterSetter = {
          get() {
            return this.data[key];
          },
          set(newValue) {
            this.data[key] = newValue;
            this.render();
          }
        };
        Object.defineProperty(this, key, getterSetter);
      });
    }

    importMethods(methods) {
      Object.entries(methods).forEach(([key, fn]) => {
        this[key] = fn;
      });
    }

    getListFromIterator(iterator) {
      let list = [];
      let current = iterator.iterateNext();
      while (current) {
        list.push(current);
        current = iterator.iterateNext();
      }
      return list;
    }

    getElementsContainingText(text) {
      const xpath = `//*[contains(text(), '${text}')]`;
      const iterator = document.evaluate(
        xpath, this.elRoot, null, XPathResult.ANY_TYPE, null
      );
      const elements = this.getListFromIterator(iterator);
      return elements;
    }

    getElementsWithAttribute(attr) {
      const elements = document.querySelectorAll(`*[${attr}]`);
      return [].slice.call(elements);
    }

    bindEvent(el, type, body) {
      const fn = Function('$event', body).bind(this);
      el.addEventListener(type, function() {
        fn(this);
      });
    }

    initBoundEventsOfType(type) {
      const elements = this.getElementsWithAttribute(`v-on\\:${type}`);
      elements.forEach((element) => {
        this.bindEvent(element, type, element.getAttribute(`v-on:${type}`));
        element.removeAttribute(`v-on:${type}`);
      });
    }

    initBoundEvents() {
      this.initBoundEventsOfType('click');
      this.initBoundEventsOfType('input');
    }

    initFragments() {
      const interpolationElements = this.getElementsContainingText(
        this.interpolationBraces[0]
      );
      interpolationElements.forEach((el) => {
        this.renderFragments.interpolation.push([el, el.innerHTML]);
      });

      const bindElements = this.getElementsWithAttribute('v-bind');
      bindElements.forEach((el) => {
        this.renderFragments.bind.push([el, el.getAttribute('v-bind')]);
        el.removeAttribute('v-bind');
      });

      const ifElements = this.getElementsWithAttribute('v-if');
      ifElements.forEach((el) => {
        this.renderFragments.if.push([el, el.getAttribute('v-if')]);
        el.removeAttribute('v-if');
      });
    }

    renderInterpolation(template) {
      const key = template
        .replace(this.interpolationBraces[0], '')
        .replace(this.interpolationBraces[1], '');
      return this.data[key];
    }

    renderAllInterpolations([el, template]) {
      const expr = new RegExp(
        `${this.interpolationBraces[0]}.*?${this.interpolationBraces[1]}`, 'g'
      );
      const matches = Array.from(template.matchAll(expr));
      matches.forEach((match) => {
        template = template.replace(match[0], this.renderInterpolation(match[0]));
      });
      el.innerHTML = template;
    }

    renderBindFragment([el, key]) {
      el.value = this[key];
    }

    renderIfFragment([el, condition]) {
      const fn = Function('return ' + condition).bind(this);
      el.hidden = !fn();
    }

    render() {
      this.renderFragments.interpolation.forEach((interpolationFragment) => {
        this.renderAllInterpolations(interpolationFragment);
      });
      this.renderFragments.bind.forEach((bindFragment) => {
        this.renderBindFragment(bindFragment);
      });
      this.renderFragments.if.forEach((ifFragment) => {
        this.renderIfFragment(ifFragment);
      });
    }
  }

  new Vue({
    el: '#vue-root',
    data: {
      name: 'Vlad',
      age: 25,
      color: '#0ff1ce',
    },
    methods: {
      setName(name) {
        this.name = name;
      },
      submit() {
        alert(JSON.stringify(this.data));
      },
    }
  });
}
