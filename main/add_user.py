from getpass import getpass
import hashlib
print("Quit with ctrl-c")

f = open("./secret", "r+")
lines = f.readlines()
try:
    while True:
        print(lines)
        username = input("New UNIQUE username >")
        if username + "\n" in lines:
            print("Username is not unique or a password hash is the same idk")
            continue
        password = hashlib.sha256(getpass().encode(), usedforsecurity=True).hexdigest()
        if password + "\n" in lines:
            print("You got a password buddy! YAY :)")

        while True:
            try:
                access_level = int(input("Access level (int, lover is more access) >"))
                break
            except ValueError:
                print("INTEGERS ONLY")

        output = [username + "\n", password + "\n", str(access_level) + "\n"]
        f.writelines(output)
        lines += output
except KeyboardInterrupt or EOFError:
    print("OK, bye")
finally:
    f.close()
