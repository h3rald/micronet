import { Mithril as m } from '../../vendor/js/mithril.js';

export class NavBarComponent {
  
  view() {
    const logo = m('section.navbar-section', [
      m('a.btn.btn-link', {
        href: '/network',
        oncreate: m.route.link,
        onupdate: m.route.link
      }, [
        m(`span.logo`, m.trust('&micro;net'))
      ])
    ]);
    return m('header.navbar', [
      logo,
      m('section.navbar-section', [
        
      ])
    ]);
  }
}
