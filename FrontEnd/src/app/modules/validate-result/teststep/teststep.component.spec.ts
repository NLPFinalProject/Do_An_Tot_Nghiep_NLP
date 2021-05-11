import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { TeststepComponent } from './teststep.component';

describe('TeststepComponent', () => {
  let component: TeststepComponent;
  let fixture: ComponentFixture<TeststepComponent>;

  beforeEach(
    waitForAsync(() => {
      TestBed.configureTestingModule({
        declarations: [TeststepComponent],
      }).compileComponents();
    })
  );

  beforeEach(() => {
    fixture = TestBed.createComponent(TeststepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
