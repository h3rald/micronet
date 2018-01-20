import { ConfigService } from './config.svc.js';
import { Mithril as m } from '../../vendor/js/mithril.js';
import { Paho } from '../../vendor/js/mqttws31.js';


let instance = null;
export class MicronetService {

  constructor(){
    if (!instance) {
      this.config = new ConfigService();
      this.onMessageArrived = this.onMessage;
      this.data = null;
      this.messages = [];
      this.connected = false;
      this.wasConnected = false;
      this.maxMessages = 100;
      instance = this;
    }
    return instance;
  }

  headers(user, pass) {
    const username = user || this.config.settings.username;
    const password = pass || this.config.settings.password;
    const credentials = btoa(`${username}:${password}`);
    return {'Authorization': `Basic ${credentials}`};
  }

  connect(settings) {
    return this._connect(settings).then((data) => {
      this.onConnectionSuccess(data);
    }).catch((data) => {
      this.onConnectionFailure(data);
    })
  }

  addMessage(msg) {
    if (this.messages.length > this.maxMessages) {
      this.messages = this.messages.pop();
    }
    this.messages.unshift(msg);
  }

  network(){
    if (this.connected) {
      return new Promise((resolve, reject) => {
        resolve(this.data);
      })
    } 
    return this.connect(this.config.settings).then(() => {
      return this.data;
    }).catch((data) => {
      this.onError(data);
    })
  }

  device(id) {
    if (this.connected) {
      return new Promise((resolve, reject) => {
        resolve(this.data.devices[id]);
      })
    } 
    return this.connect(this.config.settings).then(() => {
      return null; // not gonna be ready.
    }).catch((data) => {
      this.onError(data);
    })
  }

  onConnectionSuccess(data) {
    this.connected = true;
    this.wasConnected = true;
    this.data = {};
    this.client.subscribe('micronet/#');
  }

  onConnectionFailure(data) {
    this.connected = false;
    if (this.wasConnected) {
      setTimeout(() => {
        console.log('Reconnecting...');
        this.connect(this.config.settings);
      }, 5000)
    } else {
      this.onError(data);
    }
  }

  onMessage(msg) {
    const topic = msg.destinationName.replace(/^micronet\//, '');
    const value = JSON.parse(msg.payloadString);
    this._setProperty(topic, value);
    this.data.timestamp = Date.now();
    if (topic.match(/^devices/) && !msg.retained) {
      const device = topic.split('/')[1];
      this._setProperty(`devices/${device}/timestamp`, this.data.timestamp);
      msg.timestamp = this.data.timestamp;
      this.addMessage(msg);
    }
    m.redraw();
  }

  onError(data) {
    console.warn(data);
    m.route.set('/connect');
  }

  _connect(settings){
    settings = settings || {};
    this.config.settings = this.config.settings || {};
    const username = settings.username || this.config.settings.username;
    const password = settings.password || this.config.settings.password;
    const hostname = settings.hostname || this.config.settings.hostname;
    const port = settings.port || this.config.settings.port;
    const path = settings.path || this.config.settings.path;
    return new Promise((resolve, reject) => {
      const opts = {
        userName: username,
        password: password,
        useSSL: true,
        onSuccess: resolve,
        onFailure: reject
      }
      this.client = new Paho.MQTT.Client(settings.hostname, settings.port, settings.path, navigator.userAgent);
      this.client.onMessageArrived = (data) => this.onMessage(data);
      this.client.onConnectionLost = (data) => console.warn(data);
      this.client.connect(opts);
    });
  }

  _setProperty(path, value) {
    const props = path.split('/');
    let data = this.data;
    let count = 0;
    props.forEach((prop) => {
      count += 1;
      if (count >= props.length) {
        data[prop] = value;
      } else {
        if (!data[prop]) {
          data[prop] = {};
        }
        data = data[prop];
      }
    });
  }

 
}
