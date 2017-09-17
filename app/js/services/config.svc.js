import {ClientStoreService} from './client-store.svc.js';
import { Mithril as m } from '../../vendor/js/mithril.js';

let instance = null;

export class ConfigService {

  constructor(){
    if (!instance) {
      this.storage = new ClientStoreService();
      instance = this;
    }
    instance.settings = instance.load();
    return instance;
  }
  
  load(){
    instance.settings = instance.storage.get('config') || instance.defaults;
    instance.version = '0.1.0-dev';
    return instance.settings;
  }
  
  save(obj){
    const data = Object.assign(instance.settings, obj);
    instance.storage.set('config', data);
  }
}
