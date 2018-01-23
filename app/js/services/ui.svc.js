import { Mithril as m } from '../../vendor/js/mithril.js';

let instance = null;
export class UiService {

  constructor(){
    if (!instance) {
      instance = this;
    }
    return instance;
  }

  lastUpdate(obj) {
    return m('.last-update', `Last update: ${obj.lastUpdate()}`);
  }

  properties(obj) {
    const props = [];
    Object.keys(obj).forEach((key) => {
      props.push(m('dt', m.trust(key)));
      props.push(m('dd', obj[key]));
    });
    return m('dl', props);
  }

  icon(i) {
    return m(`i.mdi.mdi-${i}`)
  }

  tile(obj) {
    return m('.tile.tile-centered', [
      m('.tile-icon', [
        obj.icon
      ]),
      m('.tile-content', [
        m('.tile-title', obj.title),
        m('.tile-subtitle.text-gray', obj.subtitle),
      ]),
      m('.tile-action', [
       obj.action
      ])
    ])
  }

  panel(obj){
    const footer = obj.footer ? m('.panel-footer', obj.footer) : '';
    return m('.panel', [
      m('.panel-header', m('.panel-title', obj.title)),
      m('.panel-body', obj.body),
      footer
    ]);
  }

  card(obj) {
    const footer = obj.footer ? m('.card-footer', obj.footer) : '';
    return m('.card', [
      m('.card-header', [
        m('.card-title', [
          obj.title
        ]),
        m('.card-subtitle', obj.subtitle)
      ]),
      m('.card-body', obj.body),
      footer
    ]);
  }

  button(obj) {
    let content = obj.text;
    if (obj.icon) {
      content = [
        this.icon(obj.icon)
      ];
    }
    return m(`a.btn.btn-${obj.class}`, {
      href: obj.href,
      oncreate: m.route.link,
      onupdate: m.route.link
    }, content);
  }

  column(obj) {
    return m('.column.col-6.col-xs-12', obj);
  }

  columns(arr) {
    return m('.columns', arr.map((i) => this.column(i)));
  }

  meter(value) {
    return m('.meter-container', [
      m('meter.meter', {
        value: value,
        min: 0,
        max: 100,
        low: 30,
        high: 80,
        optimum: 10
      })
    ]);
  }
 
}
