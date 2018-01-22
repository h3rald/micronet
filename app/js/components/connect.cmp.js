import { ConfigService } from '../services/config.svc.js';
import { MicronetService } from '../services/micronet.svc.js';
import { FooterComponent } from './footer.cmp.js'; 
import { NavBarComponent } from './nav-bar.cmp.js';
import { Mithril as m } from '../../vendor/js/mithril.js';

export class ConnectComponent {

  constructor() {
    this.config = new ConfigService();
    this.api = new MicronetService();
    this.settings = {
      username: '',
      password: '',
      hostname: '',
      port: 8083,
      path: ''
    };
    Object.assign(this.settings, this.config.settings);
    this.failure = null;
  }

  connect() {
    this.settings.port = parseInt(this.settings.port);
    return this.api.connect(this.settings).
      then(() => {
        this.failure = '';
        this.config.save(this.settings);
        m.route.set('/home');
      }).catch(() => {
        this.failure = 'Invalid connection settings.';
      });
  }

  setUsername(value) {
    this.settings.username = value;
  }

  setPassword(value) {
    this.settings.password = value;
  }

  setHostname(value) {
    this.settings.hostname = value;
  }

  setPort(value) {
    this.settings.port = parseInt(value);
  }

  setPath(value) {
    this.settings.path = value;
  }

  view() {
    const error = (this.failure) ? m('.toast.toast-error', this.failure) : '';
    return m('article.connect', [
      m(NavBarComponent),
      m('main.connect', [
        m('h1', 'Connect'),
        error,
        m('.form-group', [
          m('label.form-label[for="hostname"', 'Host Name'),
          m('input.form-input#hostname', {
            placeholder: 'Enter the host name...',
            type: 'text',
            value: this.settings.hostname,
            oninput: m.withAttr('value', this.setHostname, this)
          })
        ]),
        m('.form-group', [
          m('label.form-label[for="port"', 'Port'),
          m('input.form-input#port', {
            placeholder: '',
            type: 'numeric',
            value: this.settings.port || 8083,
            oninput: m.withAttr('value', this.setPort, this)
          })
        ]),
        m('.form-group', [
          m('label.form-label[for="path"', 'Path'),
          m('input.form-input#path', {
            placeholder: 'Enter the path (optional)',
            type: 'text',
            value: this.settings.path,
            oninput: m.withAttr('value', this.setPath, this)
          })
        ]),
        m('.form-group', [
          m('label.form-label[for="username"', 'Username'),
          m('input.form-input#username', {
            placeholder: 'Enter the username...',
            type: 'text',
            value: this.settings.username,
            oninput: m.withAttr('value', this.setUsername, this)
          })
        ]),
        m('.form-group', [
          m('label.form-label[for="password"', 'Password'),
          m('input.form-input#password', {
            placeholder: 'Enter the password...',
            type: 'password',
            value: this.settings.password,
            oninput: m.withAttr('value', this.setPassword, this)
          })
        ]),
        m('.form-group', [
          m('button.btn.btn-primary', {
            onclick: () => { this.connect(); },
          }, 'Connect')
        ])
      ]),
      m(FooterComponent)
    ]);
  }
}
