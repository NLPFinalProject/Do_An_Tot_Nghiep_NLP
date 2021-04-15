import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
//import{User} from '@../../../src/app/login/User'

@Injectable({
  providedIn: 'root'
})
export class FileService {
  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  testform(): Observable<Object> {
    /*console.log('there');
    return this.http.get(`${this.baseUrl}/api/file/test`);*/
    return this.http.get(`${this.baseUrl}/api/file/test2`);
  }
  ExportResultToEmail(data:Object): Observable<Object> {
    /*console.log('there');
    return this.http.get(`${this.baseUrl}/api/file/test`);*/
    return this.http.post(`${this.baseUrl}/api/mail-export/export-result`,data);
  }
  UploadFile(file: File): Observable<Object> {
    const formData: FormData = new FormData();
    var id = localStorage.getItem('id');
    if (id != undefined) formData.append('id', id);
    console.log('file is 2');
    console.log(file);
    formData.append('DataDocumentFile', file);

    //formData.append('title', file.name);
    //if(localStorage.getItem('id')!=undefined)
    //  formData.append('id', localStorage.getItem('id'));
    return this.http.post(`${this.baseUrl}/api/file/uploadfile`, formData);
  }
  checkPlagiasm(data: Object): Observable<Object> {
    /*console.log('there');
    return this.http.get(`${this.baseUrl}/api/file/test`);*/
    return this.http.post(`${this.baseUrl}/api/file/test3`, data);
  }
  checkPlagiasmV2(data: Object): Observable<Object> {
    console.log('there');

    return this.http.post(`${this.baseUrl}/api/file/final-check`, data);
  }
  UploadFileList(file: FileList): Observable<Object> {
    const formData: FormData = new FormData();
    var id = localStorage.getItem('id');
    if (id != undefined) formData.append('id', id);
    for (var i = 0; i < file.length; i++) {
      let temp = file.item(i);

      formData.append('DataDocumentFile', temp);
      //formData.append('title', temp.name);

      console.log(temp.name);
    }
    //if(localStorage.getItem('id')!=undefined)
    // formData.append('id', localStorage.getItem('id'));
    return this.http.post(`${this.baseUrl}/api/file/uploadfilelist`, formData);
  }
  createUSer(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/`, user);
  }

  login(user: Object): Observable<Object> {
    console.log(`${this.baseUrl}/api/login`);
    return this.http.post(`${this.baseUrl}/login`, user);
  }

  ForgotPassword(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/forgot-password`, user);
  }

  ResetPassword(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/reset-password`, user);
  }
  /*register(user: Object): Observable<Object> {
    return this.http.post('/api/SendMail',user);
  }

  ActivateUser(user: Object): Observable<Object> {
    return this.http.post('/api/activate',user);
  }

  createUSer(user: Object): Observable<Object> {
    return this.http.post('api/', user);
  }

  login(user: Object): Observable<Object> {
    return this.http.post('api/login',user);
  }

  ForgotPassword(user: Object): Observable<Object> {
    return this.http.post('/api/forgot-password',user);
  }

  ResetPassword(user: Object): Observable<Object> {
    return this.http.post('/api/reset-password',user);
  }*/
}
