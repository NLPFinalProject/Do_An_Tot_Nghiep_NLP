export class MessageError {
  static Errors = [
    {
      name: 'required',
      text: 'This field is required',
      rules: ['touched'],
    },
    { name: 'minlength', text: 'Min length is ', rules: ['dirty'] },
  ];
  static TextError = [
    {
      password: 'Password is required',
    },
  ];
}
