def loop():
    try:
        from main import heart
        import keyboard

        heart()
    except Exception as e:
        print(f"{str(e)}")
        error = str(e)
        if str(e) == "'NoneType' object has no attribute 'keys'":
            print("<----------------No Result Found--------------->")
        elif str(e) == "no nameservers":
            print("Please Check your Internet Connection")
        elif error[0:20] == "SSL handshake failed":
            print("Your IP is not Registered")
        else:
            pass
        
        print("Press Any Key to Retry or Esc for exit")
        keyinput = keyboard.read_key()
        if keyinput=='esc':
            print("Good Luck!")
            return None
        else:
            return loop()

loop()
