import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { FileService } from '@../../../src/app/shell/shell-routing-service';

import { NzMessageService } from 'ng-zorro-antd/message';
import { UploadChangeParam } from 'ng-zorro-antd/upload';
@Component({
  selector: 'app-teststep',
  templateUrl: './teststep.component.html',
  styleUrls: ['./teststep.component.scss']
})
export class TeststepComponent implements OnInit {
  //private routeSub: Subscription;
  isvalid: boolean = false;
  public step: number;
  public UploadedFileConfirmed: false;
  FileToUpload: File = null;
  ListFileToUpload: FileList = null;
  fileList:any[];
  constructor(private route: ActivatedRoute, private router: Router, private fileService: FileService) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.step = +params['id']; // (+) converts string 'id' to a number
      console.log(this.step);
    });
    this.fileList=null;
  }
  /*nextstep() {
    //check which step it is
    if (this.step == 1) {
      this.step=this.step+1;
      this.router.navigate(['checkresult/step/2'], {
        // preserve the existing query params in the route

        // do not trigger navigation
        replaceUrl: true
      });
    } else if (this.step == 2) 
    {
      let id = localStorage.getItem('id');
      let filename1= localStorage.getItem('file');
      let data={
        'id':id,
        'filename1':filename1,
        'listfile':this.fileList,
      }

      //this.router.navigate(['checkresult/result'], { replaceUrl: true });
      this.fileService.checkPlagiasm(data).subscribe((data:any)=>
      {
        console.log('data is');
        console.log(data);
        console.log('-----------')
        this.router.navigate(['checkresult/result'],{ replaceUrl: true, state: { data: data } });
      })
  }
  }*/
  nextstep() {
    //check which step it is
    if (this.step == 1) {
      this.step=this.step+1;
      this.uploadFile();
      this.isvalid= false;
      this.router.navigate(['checkresult/step/2'], {
          // preserve the existing query params in the route
  
          // do not trigger navigation
          replaceUrl: true
        });
     
      
    } else if (this.step == 2) 
    {
      
      this.fileService.UploadFileList(this.ListFileToUpload).subscribe((data:any) => {
      console.log('hhhhh');
      let id = localStorage.getItem('id');
      let filename1= localStorage.getItem('file');
      this.fileList=data.data;
      let tempdata={
        'id':id,
        'filename1':filename1,
        'listfile':this.fileList,
      }
        
        this.fileService.checkPlagiasm(tempdata).subscribe((data:any)=>
      {
        console.log('data is');
        console.log(data);
        console.log('-----------')
        this.router.navigate(['checkresult/result'],{ replaceUrl: true, state: { data: data } });
      })
        
      });
      //this.router.navigate(['checkresult/result'], { replaceUrl: true });
      
  }
  }
  upload = (file: any) => {
    console.log('welcome');
    console.log(file.name);
    console.log(file);
    /*setTimeout(() => {
    file.onProgress({ percent: 50 });
    setTimeout(() => {
      const dataFile = {
        name: file.file.name,
        status: 'Thành công'
      };
      this.data.push(dataFile);
      // notify success
      file.onSuccess();
      this.displayData = [...this.data];
      this.messageService.success('Thêm tệp tin thành công');
    }, 500);
  }, 10);*/
    // tslint:disable-next-line:semicolon
    this.fileService.UploadFile(file);
  };
  uploadFile = () => {
    console.log('welcome');
    /*console.log(file.name);
  console.log(file);
  this.FileToUpload = file;*/

    /*setTimeout(() => {
    file.onProgress({ percent: 50 });
    setTimeout(() => {
      const dataFile = {
        name: file.file.name,
        status: 'Thành công'
      };
      this.data.push(dataFile);
      // notify success
      file.onSuccess();
      this.displayData = [...this.data];
      this.messageService.success('Thêm tệp tin thành công');
    }, 500);
  }, 10);*/
    this.fileService.UploadFile(this.FileToUpload).subscribe(data => {
      console.log('data is');
      let t= JSON.stringify(data);
      localStorage.setItem('file',t);


      
    });
    // tslint:disable-next-line:semicolon
  };
  uploadFileList = () => {
    /*setTimeout(() => {
    file.onProgress({ percent: 50 });
    setTimeout(() => {
      const dataFile = {
        name: file.file.name,
        status: 'Thành công'
      };
      this.data.push(dataFile);
      // notify success
      file.onSuccess();
      this.displayData = [...this.data];
      this.messageService.success('Thêm tệp tin thành công');
    }, 500);
  }, 10);*/
    this.fileService.UploadFileList(this.ListFileToUpload).subscribe((data:any) => {
      console.log('hhhhh');
      
      this.fileList=data.data;
      
      
    });
    console.log('fail');
    // tslint:disable-next-line:semicolon
  };

  /*handleChange(info: UploadChangeParam): void {
  this.uploadFileList(null);
  if (info.file.status !== 'uploading') {
    console.log(info.file, info.fileList);
  }
  if (info.file.status === 'done') {
    this.msg.success(`${info.file.name} file uploaded successfully`);
  } else if (info.file.status === 'error') {
    this.msg.error(`${info.file.name} file upload failed.`);
  }
}*/
  handleChangeFile(file: FileList): void {
    console.log('hi there');
    this.FileToUpload = file.item(0);
    this.uploadFile();
   
    
  }
  handleChangeFileV1(file: FileList): void {
    
    this.FileToUpload = file.item(0);
    this.isvalid = true;
   
    
  }
  handleChangeFile1 = (item: any) => {
    console.log('hi there');
    this.FileToUpload = item.item(0);
    this.uploadFile();
    
  };

  handleChangeFileList(file: FileList): void {
    
    this.ListFileToUpload = file;
    this.isvalid = true;
    //this.uploadFileList();
    //console.log('here');
  }
}
