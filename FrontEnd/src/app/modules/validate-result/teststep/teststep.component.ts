import { Component, OnInit, Inject } from '@angular/core';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
import { FormControl } from '@angular/forms';
import { NzMessageService } from 'ng-zorro-antd/message';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

import { NgxFileDropEntry, FileSystemFileEntry, FileSystemDirectoryEntry } from 'ngx-file-drop';
export interface DialogData {
  animal: string;
  name: string;
}
@Component({
  selector: 'app-teststep',
  templateUrl: './teststep.component.html',
  styleUrls: ['./teststep.component.scss'],
})
export class TeststepComponent implements OnInit {
  //private routeSub: Subscription;
  requestData: any;
  agreeStatus: Boolean;
  isvalid: boolean = false;
  public step: number;
  public UploadedFileConfirmed: false;
  public isSpinning: boolean = false;
  FileToUpload: File = null;
  ListFileToUpload: FileList = null;
  ListOfFile: File[];
  public files: NgxFileDropEntry[] = [];
  fileList: any[];
  public step1Unlock: boolean = false;

  public selectedOption: number;
  option: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private fileService: FileService,
    public dialog: MatDialog
  ) {}

  ngOnInit() {
    this.route.params.subscribe((params) => {
      this.step = 1; // (+) converts string 'id' to a number
      console.log(this.step);
    });
    this.ListOfFile = [];
    this.fileList = null;
    this.selectedOption = 1;
    this.option = '1';
  }
  ngOnDestroy() {
    console.log('now you die');
  }
  HandleSelectionChange(id: any) {
    console.log(id);
    this.step = 2;
    this.isvalid = true;
    this.selectedOption = parseInt(id);
    if (this.selectedOption == 1) {
      this.step1Unlock = true;
    } else {
      this.files = [];
      this.ListOfFile = null;
      this.step1Unlock = false;
    }
    //this.step2Unlock=true;
  }

  HandleSelectionSaveFileChange(isSave: string) {
    if (isSave == 'yes') {
      this.agreeStatus = true;
    } else {
      this.agreeStatus = false;
    }
  }

  nextstep() {
    //check which step it is
    if (this.step == 1) {
      //this.step1Unlock = true;
      this.isSpinning = true;
      this.step = this.step + 1;
      console.log('data is');
      this.isSpinning = false;
      console.log(this.isSpinning);
      localStorage.setItem('file', this.FileToUpload.name);
      this.isvalid = false;
      this.step = 2;
      localStorage.setItem('choice', this.selectedOption.toString());
      console.log('now');
      if (this.selectedOption == 1) {
        this.step1Unlock = true;
      }
    } else if (this.step == 2) {
      this.isSpinning = true;
      //this.fileService.UploadFileList(this.ListFileToUpload).subscribe((data: any) => {

      console.log('hhhhh');

      let id = localStorage.getItem('id');
      //let choice = parseInt(localStorage.getItem('choice'));
      let choice = this.selectedOption;
      //let filename1 = localStorage.getItem('file');
      this.fileList = this.ListOfFile;
      console.log('choice is', choice);
      switch (choice) {
        case 1: {
          if (this.ListOfFile != null) {
            let tempdata = {
              id: id,
              filename1: this.FileToUpload,
              listfile: this.fileList,

              agreeStatus: this.agreeStatus,
            };
            console.log(tempdata);
            this.fileService.checkPlagiasmNormal(tempdata).subscribe((data: any) => {
              console.log(data);
              this.openDialog();
            });
          } else {
            //add warning here
          }

          //   console.log(data);
          //   this.router.navigate(['checkresult/result'], { replaceUrl: true, state: { data: data } });
          // })
          break;
        }
        case 2: {
          let tempdata = {
            id: id,
            filename1: this.FileToUpload,
            //listfile: this.fileList,

            agreeStatus: this.agreeStatus,
          };
          this.fileService.checkPlagiasmUsingDatabase(tempdata).subscribe((data: any) => {
            console.log(data);
            this.openDialog();
          });
          console.log(tempdata);
          //this.openDialog();
          break;
        }
        case 3: {
          let tempdata = {
            id: id,
            filename1: this.FileToUpload,
            //listfile: this.fileList,

            agreeStatus: this.agreeStatus,
          };
          this.fileService.checkPlagiasmUsingInternet(tempdata).subscribe((data: any) => {
            console.log(data);
            console.log('done my job');
          });
          this.openDialog();

          break;
        }
        case 4: {
          let tempdata = {
            id: id,
            filename1: this.FileToUpload,
            //listfile: this.fileList,

            agreeStatus: this.agreeStatus,
          };
          // this.fileService.checkPlagiasmUsingAll2(tempdata).subscribe((data:any)=>{
          //   console.log(data);
          //   this.router.navigate(['checkresult/result'], { replaceUrl: true, state: { data: data } });
          // })
          console.log(tempdata);
          break;
        }
      }
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
      this.fileList = data.data;
    });
    console.log('fail');
    // tslint:disable-next-line:semicolon
  };

  handleChangeFile(file: FileList): void {
    this.FileToUpload = file.item(0);
    this.isvalid = true;
  }
  handleChangeFile1 = (item: File) => {
    console.log('hi there');
    this.FileToUpload = item;
    this.uploadFile();
  };
  WarningSize() {
    const dialogRef = this.dialog.open(WarningFileSizeDialog, {
      width: '250px',
      //data: {name: this.name, animal: this.animal}
    });
  }
  handleChangeFileList(file: FileList): void {
    this.ListFileToUpload = file;
    this.isvalid = true;
    //this.uploadFileList();
    //console.log('here');
  }
  public droppedFile(files: NgxFileDropEntry[]) {
    //this.isvalid = true;

    console.log('busted');
    if (files[0].fileEntry.isFile) {
      const fileEntry = files[0].fileEntry as FileSystemFileEntry;
      fileEntry.file((file: File) => {
        if (file.size > 10 * 1024 * 1024) {
          this.WarningSize();
        }
        // Here you can access the real file
        else {
          this.FileToUpload = file;
        }

        //this.ListOfFile.push(file);
      });
    }
  }

  public dropped(files: NgxFileDropEntry[]) {
    //this.isvalid = true;

    this.files = files;
    for (const droppedFile of files) {
      // Is it a file?
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file((file: File) => {
          console.log(1);
          // Here you can access the real file
          if (file.size <= 10 * 1024 * 1024) {
            console.log(file);
            this.ListOfFile.push(file);
          } else {
            this.ListOfFile = null;
            this.WarningSize();
          }

          //this.handleChangeFile1(file);
          //this.FileToUpload=null;
          /**
            // You could upload it like this:
            const formData = new FormData()
            formData.append('logo', file, relativePath)
  
            // Headers
            const headers = new HttpHeaders({
              'security-token': 'mytoken'
            })
  
            this.http.post('https://mybackend.com/api/upload/sanitize-and-save-logo', formData, { headers: headers, responseType: 'blob' })
            .subscribe(data => {
              // Sanitized logo returned from backend
            })
            **/
        });
      } else {
        // It was a directory (empty directories are added, otherwise only files)
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
        console.log(droppedFile.relativePath, fileEntry);
      }
    }
  }
  openDialog(): void {
    const dialogRef = this.dialog.open(SuccessUploadDialog, {
      width: '250px',
      //data: {name: this.name, animal: this.animal}
    });

    dialogRef.afterClosed().subscribe((result) => {
      console.log('The dialog was closed');
    });
  }
  public fileOver(event: any) {
    console.log(3);
    console.log(event);
  }
  openFileSelector() {
    console.log(1);
    console.log('wow');
  }

  public fileLeave(event: any) {
    console.log(2);
    console.log(event);
  }
}
@Component({
  selector: 'success-upload-dialog',
  templateUrl: 'success-upload-dialog.html',
})
export class SuccessUploadDialog {
  constructor(
    public dialogRef: MatDialogRef<SuccessUploadDialog>,
    private router: Router,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
    let value = localStorage.getItem('username');
    this.router.navigate(['daovan'], { replaceUrl: true, state: { user: value } });
  }
}

@Component({
  selector: 'warning-size-dialog',
  templateUrl: 'warning-size-dialog.html',
})
export class WarningFileSizeDialog {
  constructor(
    public dialogRef: MatDialogRef<WarningFileSizeDialog>,

    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  ConfirmClick(): void {
    this.dialogRef.close();
    // let value = localStorage.getItem('username');
    // this.router.navigate(['daovan'], { replaceUrl: true, state: { user: value } });
  }
}
