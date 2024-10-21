📚 JOOR / Cin7 Integration

Integration for JOOR. Built using the V4 and V2 API. Meant as a one way order flow besides Orders

Consist of:

    🟢 Products
    🟢 Orders
    🟢 Customers
    ...


🛑 Issues to be aware of

    To be added

Comments

    A look into Windows Defender might be warranted since it can also interfere with our program's execution, so make sure to set exclusions accordingly.
    You get a reverse shell or something after injecting a remote target process and for the first few seconds, it's fine. Then, the second you issue a command, Windows Defender (or some other security solution) kills your process/connection. This can be due to how signatured (msfvenom | metasploit) payloads, listeners, handlers, etc. are. Encrypt your traffic or use something less signatured. A reverse shell by itself is almost always suspicious so more techniques are going to be needed in conjunction with what we've learned above.
    The (in)direct syscalls technique isn't working! This could be due to API Hooking. EDRs/security solutions will sometimes inject their own DLL into your process to hook commonly abused functions. The function(s) responsible for scraping the syscall numbers and instructions currently don't incorporate a way to fight/circumnavigate API Hooking and will fall apart due to the offsets being borked. So, you're going to have to be stuck in limbo for a while and research how to do that yourself. Eventually (TM), I'll add a way to account for hooks, in which case, I'll just remove this line from the common pitfalls section.
