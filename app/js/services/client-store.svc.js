let instance = null;

export class ClientStoreService {

  constructor(){
    if (!instance) {
      this.storage = window.localStorage;
      instance = this;
    }
    return instance;
  }
  
  set(id, data){
    this.storage.setItem(id, JSON.stringify(data));
  }
  
  get(id){
    try {
      return JSON.parse(this.storage.getItem(id));
    } catch(e) {
      return null;
    }
  }
  
  del(id){
    this.storage.removeItem(id);
  }
  
}
