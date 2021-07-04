import { Component, OnInit, Inject } from '@angular/core';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
import { FormControl } from '@angular/forms';
import { NzMessageService } from 'ng-zorro-antd/message';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { AuthenticationService } from '../../../core/authentication/authentication.service';

import { NgxFileDropEntry, FileSystemFileEntry, FileSystemDirectoryEntry } from 'ngx-file-drop';
import { LockUserDialog } from '@app/modules/administrator/list-account/list-account.component';
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
  public isFirstFileValid: boolean = false;
  public step: number;
  public UploadedFileConfirmed: false;
  public isSpinning: boolean = false;
  FileToUpload: File = null;
  ListFileToUpload: FileList = null;
  ListOfFile: File[];
  public files: NgxFileDropEntry[] = [];
  fileList: any[];
  public step1Unlock: boolean = false;
  public changeNameStatus: boolean = false;
  public selectedOption: number;
  sessionName: string = '';
  option: string;
  public validEndFile = ['.doc', '.docx', '.pdf', '.xlsx', '.csv', '.pptx', '.txt'];
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private fileService: FileService,
    public dialog: MatDialog,
    private authenticationService: AuthenticationService
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
  HandleSelectionChangeName(id: any) {
    if (id == '1') {
      this.changeNameStatus = true;
    } else {
      this.changeNameStatus = false;
    }
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
      console.log(this.sessionName);
      switch (choice) {
        case 1: {
          if (this.ListOfFile != null) {
            let tempdata = {
              id: id,
              filename1: this.FileToUpload,
              listfile: this.fileList,
              sessionName: this.sessionName,
              agreeStatus: this.agreeStatus,
            };
            console.log(tempdata);
            this.fileService.checkPlagiasmNormal(tempdata).subscribe(
              (data: any) => {
                if (data != null) {
                  console.log(data);
                  if (data == localStorage.getItem('id')) {
                    this.SuccessDialog();
                  } else {
                    console.log('fail');
                  }
                }
              },
              (error) => {
                if (error.error == 'user_is_lock') {
                  this.UserIsLockedDialog();
                } else if (error.error == 'fail status') {
                  this.CommonProblemDialog();
                }
              }
            );
            this.router.navigate(['daovan'], { replaceUrl: true });
            //this.openDialog();
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
            sessionName: this.sessionName,
            agreeStatus: this.agreeStatus,
          };
          this.fileService.checkPlagiasmUsingDatabase(tempdata).subscribe(
            (data: any) => {
              if (data != null) {
                console.log(data);
                if (data == localStorage.getItem('id')) {
                  this.SuccessDialog();
                } else {
                  console.log('fail');
                }
              }
            },
            (error) => {
              if (error.error == 'user_is_lock') {
                this.UserIsLockedDialog();
              } else if (error.error == 'fail status') {
                this.CommonProblemDialog();
              }
            }
          );
          console.log(tempdata);
          //this.SuccessDialog();
          //this.openDialog();
          this.router.navigate(['daovan'], { replaceUrl: true });
          break;
        }
        case 3: {
          let tempdata = {
            id: id,
            filename1: this.FileToUpload,
            //listfile: this.fileList,
            sessionName: this.sessionName,
            agreeStatus: this.agreeStatus,
          };
          this.fileService.checkPlagiasmUsingInternet(tempdata).subscribe(
            (data: any) => {
              if (data != null) {
                console.log(data);
                if (data == localStorage.getItem('id')) {
                  this.SuccessDialog();
                } else {
                  console.log('fail');
                }
              }
            },
            (error) => {
              if (error.error == 'user_is_lock') {
                this.UserIsLockedDialog();
              }
            }
          );
          //this.openDialog();
          this.router.navigate(['daovan'], { replaceUrl: true });

          break;
        }
        case 4: {
          let tempdata = {
            id: id,
            filename1: this.FileToUpload,
            //listfile: this.fileList,
            sessionName: this.sessionName,
            agreeStatus: this.agreeStatus,
          };
          this.fileService.checkPlagiasmUsingAll(tempdata).subscribe(
            (data: any) => {
              if (data != null) {
                console.log(data);
                if (data == localStorage.getItem('id')) {
                  this.SuccessDialog();
                } else {
                  console.log('fail');
                }
              }
            },
            (error) => {
              if (error.error == 'user_is_lock') {
                this.UserIsLockedDialog();
              } else if (error.error == 'fail status') {
                this.CommonProblemDialog();
              }
            }
          );

          //this.openDialog();
          this.router.navigate(['daovan'], { replaceUrl: true });
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
  WarningInvalidFile() {
    const dialogRef = this.dialog.open(WarningInvalidFileDialog, {
      width: '250px',
      //data: {name: this.name, animal: this.animal}
    });
  }
  SuccessDialog() {
    const dialogRef = this.dialog.open(SuccessTransition, {
      width: '250px',
      //data: {name: this.name, animal: this.animal}
    });
  }
  UserIsLockedDialog() {
    const dialogRef = this.dialog.open(UserIsLockedDialog, {
      width: '250px',
      //data: {name: this.name, animal: this.animal}
    });
  }
  CommonProblemDialog() {
    const dialogRef = this.dialog.open(CommonProblemDialog, {
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
  checkValidFile(name: string) {
    console.log('in here');
    var position = name.lastIndexOf('.');
    if (position == -1) return false;
    var endFile = name.substr(position, name.length - position);
    console.log(endFile);
    if (this.validEndFile.indexOf(endFile) == -1) return false;
    return true;
  }
  public droppedFile(files: NgxFileDropEntry[]) {
    //this.isvalid = true;

    if (files[0].fileEntry.isFile) {
      const fileEntry = files[0].fileEntry as FileSystemFileEntry;
      fileEntry.file((file: File) => {
        if (file.size > 10 * 1024 * 1024) {
          this.isFirstFileValid = false;
          this.WarningSize();
          this.files.splice(0);
        } else if (!this.checkValidFile(file.name)) {
          this.isFirstFileValid = false;
          this.WarningInvalidFile();
          this.files.splice(0);
          this.FileToUpload = null;
        }
        // Here you can access the real file
        else {
          this.isFirstFileValid = true;
          this.FileToUpload = file;
        }

        //this.ListOfFile.push(file);
      });
    }
  }

  public dropped(files: NgxFileDropEntry[]) {
    //this.isvalid = true;
    var flagValidFile = true;
    this.files = files;
    for (const droppedFile of files) {
      // Is it a file?
      if (flagValidFile) {
        if (droppedFile.fileEntry.isFile) {
          const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
          fileEntry.file((file: File) => {
            console.log(1);
            // Here you can access the real file
            if (!this.checkValidFile(file.name)) {
              this.WarningInvalidFile();
              this.ListOfFile = [];
              flagValidFile = false;
            } else if (file.size <= 10 * 1024 * 1024) {
              console.log(file);

              this.ListOfFile.push(file);
            } else {
              console.log('no problem');
              this.ListOfFile = [];
              //this.fi
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
      } else {
        break;
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
@Component({
  selector: 'invalid-file-dialog',
  templateUrl: 'invalid-file-dialog.html',
})
export class WarningInvalidFileDialog {
  constructor(
    public dialogRef: MatDialogRef<WarningInvalidFileDialog>,

    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  ConfirmClick(): void {
    this.dialogRef.close();

    // let value = localStorage.getItem('username');
    // this.router.navigate(['daovan'], { replaceUrl: true, state: { user: value } });
  }
}
@Component({
  selector: 'success-validate-dialog',
  templateUrl: 'success-validate-dialog.html',
})
export class SuccessTransition {
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
@Component({
  selector: 'user-is-locked-dialog',
  templateUrl: 'user-is-locked-dialog.html',
})
export class UserIsLockedDialog {
  constructor(
    public dialogRef: MatDialogRef<UserIsLockedDialog>,
    private authenticationService: AuthenticationService,
    private router: Router,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  ConfirmClick(): void {
    this.dialogRef.close();
    this.authenticationService.logout().subscribe(() => this.router.navigate(['/login'], { replaceUrl: true }));

    // let value = localStorage.getItem('username');
    // this.router.navigate(['daovan'], { replaceUrl: true, state: { user: value } });
  }
}
@Component({
  selector: 'common-problem-dialog',
  templateUrl: 'common-problem-dialog.html',
})
export class CommonProblemDialog {
  constructor(
    public dialogRef: MatDialogRef<CommonProblemDialog>,

    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  ConfirmClick(): void {
    this.dialogRef.close();
    // let value = localStorage.getItem('username');
    // this.router.navigate(['daovan'], { replaceUrl: true, state: { user: value } });
  }
}
