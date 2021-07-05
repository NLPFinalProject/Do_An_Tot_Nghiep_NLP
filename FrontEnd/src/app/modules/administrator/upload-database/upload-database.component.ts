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
  selector: 'app-upload-database',
  templateUrl: './upload-database.component.html',
  styleUrls: ['./upload-database.component.scss'],
})
export class UploadDatabaseComponent implements OnInit {
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
    });
    this.ListOfFile = [];
    this.fileList = null;
    this.selectedOption = 1;
    this.option = '1';
  }
  ngOnDestroy() {}

  WarningSize() {
    const dialogRef = this.dialog.open(WarningFileSizeDialog, {
      width: '250px',
    });
  }
  public droppedFile(files: NgxFileDropEntry[]) {
    if (files[0].fileEntry.isFile) {
      const fileEntry = files[0].fileEntry as FileSystemFileEntry;
      fileEntry.file((file: File) => {
        if (file.size > 10 * 1024 * 1024) {
          this.WarningSize();
        } else {
          this.FileToUpload = file;
        }

        //this.ListOfFile.push(file);
      });
    }
  }
  uploadList() {
    this.fileService.UploadFileList2(this.ListOfFile).subscribe((data: any) => {
      this.openDialog();
    });
    this.router.navigate(['daovan'], { replaceUrl: true });
  }
  public dropped(files: NgxFileDropEntry[]) {
    //this.isvalid = true;
    this.isvalid = true;
    this.files = files;
    for (const droppedFile of files) {
      // Is it a file?
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file((file: File) => {
          // Here you can access the real file
          if (file.size <= 10 * 1024 * 1024) {
            this.ListOfFile.push(file);
          } else {
            this.ListOfFile = [];
            this.WarningSize();
          }
        });
      } else {
        // It was a directory (empty directories are added, otherwise only files)
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
      }
    }
  }
  openDialog(): void {
    const dialogRef = this.dialog.open(SuccessUploadDialog, {
      width: '250px',
      //data: {name: this.name, animal: this.animal}
    });

    dialogRef.afterClosed().subscribe((result) => {});
  }
  public fileOver(event: any) {}
  openFileSelector() {}

  public fileLeave(event: any) {}
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
