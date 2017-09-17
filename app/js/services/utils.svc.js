let instance = null;
export class UtilsService {

  constructor(){
    if (!instance) {
      instance = this;
    }
    return instance;
  }

  prop(obj, path){
    if (!obj) {
      return '';
    }
    const props = path.split('.');
    let data = obj;
    for (let c=0; c<props.length; c++) {
      const p = data[props[c]];
      if (p !== null && p !== undefined) {
        data = data[props[c]];
      }
      else {
        data = '';
        break;
      }
    }
    return data;
  }
}
