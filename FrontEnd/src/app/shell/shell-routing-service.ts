import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
//import{User} from '@../../../src/app/login/User'

@Injectable({
  providedIn: 'root',
})
export class FileService {
  private baseUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  getResult(data: any): Observable<Object> {
    let param = new HttpParams();
    let data1 = {
      id: localStorage.getItem('id'),
      sessionId: data,
    };
    param.set('id', localStorage.getItem('id'));
    param.set('sessionId', data);

    return this.http.post(`${this.baseUrl}/api/file/getjsonresult`, data1);
  }
  ExportResultToEmail(data: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/mail-export/export-result`, data);
  }
  UploadFile(file: File): Observable<Object> {
    const formData: FormData = new FormData();
    var id = localStorage.getItem('id');
    if (id != undefined) formData.append('id', id);
    formData.append('DataDocumentFile', file);
    return this.http.post(`${this.baseUrl}/api/file/uploadfile`, formData);
  }
  checkPlagiasm(data: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/file/test3`, data);
  }
  checkPlagiasmNormal(data: any): Observable<Object> {
    const formData: FormData = new FormData();
    formData.append('agreeStatus', data.agreeStatus);
    formData.append('id', data.id);
    formData.append('DataDocumentFile', data.filename1);
    formData.append('sessionName', data.sessionName);
    let file = data.listfile;
    for (var i = 0; i < file.length; i++) {
      let temp = file[i];

      formData.append('DataDocumentFileList', temp);
    }
    return this.http.post(`${this.baseUrl}/api/file/test3`, formData);
  }
  checkPlagiasmUsingDatabase(data: any): Observable<Object> {
    const formData: FormData = new FormData();

    formData.append('id', data.id);

    formData.append('agreeStatus', data.agreeStatus);
    formData.append('sessionName', data.sessionName);
    formData.append('DataDocumentFile', data.filename1);

    return this.http.post(`${this.baseUrl}/api/file/checkdatabase`, formData);
  }
  checkPlagiasmUsingAll(data: any): Observable<Object> {
    const formData: FormData = new FormData();
    formData.append('id', data.id);
    formData.append('agreeStatus', data.agreeStatus);
    formData.append('sessionName', data.sessionName);
    formData.append('DataDocumentFile', data.filename1);
    return this.http.post(`${this.baseUrl}/api/file/checkdatabaseinternet`, formData);
  }
  checkPlagiasmUsingInternet(data: any): Observable<Object> {
    const formData: FormData = new FormData();

    formData.append('id', data.id);
    formData.append('sessionName', data.sessionName);
    formData.append('agreeStatus', data.agreeStatus);

    formData.append('DataDocumentFile', data.filename1);

    return this.http.post(`${this.baseUrl}/api/file/checkinternet`, formData);
  }

  checkPlagiasmV2(data: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/file/final-check`, data);
  }

  UploadFileList(file: FileList): Observable<Object> {
    const formData: FormData = new FormData();
    var id = localStorage.getItem('id');
    if (id != undefined) formData.append('id', id);
    for (var i = 0; i < file.length; i++) {
      let temp = file.item(i);

      formData.append('DataDocumentFileList', temp);
    }

    return this.http.post(`${this.baseUrl}/api/file/uploadfilelist`, formData);
  }
  UploadFileList2(file: File[]): Observable<Object> {
    const formData: FormData = new FormData();
    var id = localStorage.getItem('id');
    if (id != undefined) formData.append('id', id);
    for (var i = 0; i < file.length; i++) {
      let temp = file[i];

      formData.append('DataDocumentFileList', temp);
      //formData.append('title', temp.name);
    }
    //if(localStorage.getItem('id')!=undefined)
    // formData.append('id', localStorage.getItem('id'));
    return this.http.post(`${this.baseUrl}/api/file/uploadfilelist`, formData);
  }
  /*createUSer(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/`, user);
  }

  login(user: Object): Observable<Object> {
  
    return this.http.post(`${this.baseUrl}/login`, user);
  }

  ForgotPassword(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/forgot-password`, user);
  }

  ResetPassword(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}/api/reset-password`, user);
  }*/
}
