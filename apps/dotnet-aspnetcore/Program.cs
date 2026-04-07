using System.Reflection;
using System.Runtime.InteropServices;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

var portValue = Environment.GetEnvironmentVariable("PORT");
if (!string.IsNullOrWhiteSpace(portValue) && int.TryParse(portValue, out var port))
{
    builder.WebHost.UseUrls($"http://0.0.0.0:{port}");
}

var app = builder.Build();

app.MapGet("/", (IConfiguration configuration, IWebHostEnvironment environment) => Results.Ok(new
{
    application = configuration["Application:Name"] ?? "GuideApi",
    environment = environment.EnvironmentName,
    runtime = RuntimeInformation.FrameworkDescription,
    assembly = Assembly.GetExecutingAssembly().GetName().Version?.ToString() ?? "unknown",
    region = Environment.GetEnvironmentVariable("AWS_REGION") ?? configuration["Application:Region"] ?? "not-set",
    port = Environment.GetEnvironmentVariable("PORT") ?? "5000",
    status = "running",
    timestamp = DateTimeOffset.UtcNow
}));

app.MapControllers();

app.Run();

public partial class Program;
