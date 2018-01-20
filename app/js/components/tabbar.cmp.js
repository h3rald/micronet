import {Mithril as m} from '../../vendor/js/mithril.js';

export class TabBarComponent {
  
  constructor(vnode){
    this.onbeforeupdate(vnode);
  }

  onbeforeupdate(vnode) {
    this.tabs = vnode.attrs.tabs || [];
    this.length = this.tabs.length;
  }

  displayTab(tab) {
    return m(`.app-tab.column.col-${12/this.length}${tab.selected ? '.selected' : ''}`, {
      onclick: () => tab.callback()
    },[
      m(`i.app-tab-icon.mdi.mdi-${tab.icon}`),
      m('div.app-tab-text', tab.title)
    ])
  }
  
  view(){
    if (this.length == 0) {
      return '';
    }
    return m('.container.app-tabs', [
      m('.columns', this.tabs.map((t) => this.displayTab(t)))
    ]);
  }
}
