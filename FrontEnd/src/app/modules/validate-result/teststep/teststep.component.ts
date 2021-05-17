import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
import { FormControl } from '@angular/forms';
import { NzMessageService } from 'ng-zorro-antd/message';
import { UploadChangeParam } from 'ng-zorro-antd/upload';
import { NgxFileDropEntry, FileSystemFileEntry, FileSystemDirectoryEntry } from 'ngx-file-drop';
@Component({
  selector: 'app-teststep',
  templateUrl: './teststep.component.html',
  styleUrls: ['./teststep.component.scss'],
})
export class TeststepComponent implements OnInit {
  //private routeSub: Subscription;
  isvalid: boolean = false;
  public step: number;
  public UploadedFileConfirmed: false;
  public isSpinning: boolean = false;
  FileToUpload: File = null;
  ListFileToUpload: FileList = null;
  fileList: any[];
  public selectedOption: number;
  option: string;

  constructor(private route: ActivatedRoute, private router: Router, private fileService: FileService) {}

  ngOnInit() {
    this.route.params.subscribe((params) => {
      this.step = +params['id']; // (+) converts string 'id' to a number
      console.log(this.step);
    });
    this.fileList = null;
    this.selectedOption = 1;
    this.option = '1';
  }
  HandleSelectionChange(id: string) {
    this.option = id;
  }

  checkChoice2(value: string) {
    console.log(value);
    this.selectedOption = parseInt(value);
    console.log(this.selectedOption);
    //this.selectedOption=parseInt(this.selectedOption)
    switch (this.selectedOption) {
      case 1: {
        localStorage.setItem('userchoice', this.selectedOption.toString());
        //get next move
        this.nextstep();
        break;
      }
      case 2: {
        let data = {
          id: localStorage.getItem('id'),
          filename1: localStorage.getItem('file'),
          choice: this.selectedOption,
        };
        this.fileService.checkPlagiasmUsingDatabase(data).subscribe((data: any) => {
          console.log('data is');
          console.log(data);
          console.log('-----------');
          this.router.navigate(['checkresult/result'], { replaceUrl: true, state: { data: data } });
        });
        break;
      }
      case 3: {
        let id = localStorage.getItem('id');

        let data = {
          id: id,
          fileName1: localStorage.getItem('file'),
          choice: this.selectedOption,
        };
        console.log('hi');
        this.fileService.checkPlagiasmUsingInternet(data).subscribe((data: any) => {
          console.log(data);
          this.router.navigate(['checkresult/result'], { replaceUrl: true, state: { data: data } });
        });
        break;
      }

      case 4: {
        let id = localStorage.getItem('id');

        let data = {
          id: id,
          fileName1: localStorage.getItem('file'),
          choice: this.selectedOption,
        };
        console.log('hi');
        this.fileService.checkPlagiasmUsingAll(data).subscribe((data: any) => {
          console.log(data);
          this.router.navigate(['checkresult/result'], { replaceUrl: true, state: { data: data } });
        });
        break;
      }
    }
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
      this.isSpinning = true;
      this.step = this.step + 1;
      this.fileService.UploadFile(this.FileToUpload).subscribe((data: string) => {
        console.log('data is');
        this.isSpinning = false;
        console.log(this.isSpinning);
        localStorage.setItem('file', data);
        this.isvalid = false;
        this.router.navigate(['checkresult/step/2'], {
          // preserve the existing query params in the route

          // do not trigger navigation
          replaceUrl: true,
        });
      });
    } else if (this.step == 2) {
      this.router.navigate(['checkresult/step/3'], {
        // preserve the existing query params in the route

        // do not trigger navigation
        replaceUrl: true,
      });

      /*this.router.navigate(['checkresult/step/3'], {
        // preserve the existing query params in the route

        // do not trigger navigation
        replaceUrl: true
      });*/
    } else if (this.step == 3) {
      this.isSpinning = true;
      this.fileService.UploadFileList(this.ListFileToUpload).subscribe((data: any) => {
        console.log('hhhhh');

        let id = localStorage.getItem('id');
        let choice = parseInt(localStorage.getItem('choice'));
        let filename1 = localStorage.getItem('file');
        this.fileList = data.data;
        console.log(data);
        let tempdata = {
          id: id,
          filename1: filename1,
          listfile: this.fileList,
          choice: choice,
        };
        console.log(tempdata);
        this.fileService.checkPlagiasm(tempdata).subscribe((data: any) => {
          this.isSpinning = false;
          console.log('data is');
          console.log(data);
          console.log('-----------');
          this.router.navigate(['checkresult/result'], { replaceUrl: true, state: { data: data } });
        });
      });
      //this.router.navigate(['checkresult/result'], { replaceUrl: true });
    }
  }
  upload = (file: any) => {
    console.log('welcome');
    console.log(file.name);
    console.log(file);

    // tslint:disable-next-line:semicolon
    this.fileService.UploadFile(file);
  };
  uploadFile = () => {
    console.log('welcome');

    this.fileService.UploadFileList(this.ListFileToUpload).subscribe((data: any) => {
      console.log('hhhhh');

      this.fileList = data.data;
    });
    console.log('fail');
    // tslint:disable-next-line:semicolon
  };
  uploadFileV1 = () => {
    console.log('welcome');

    this.fileService.UploadFile(this.FileToUpload).subscribe((data: any) => {
      console.log('hhhhh');

      this.fileList = data.data;
    });
    console.log('fail');
    // tslint:disable-next-line:semicolon
  };

  handleChangeFile(file: FileList): void {
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
